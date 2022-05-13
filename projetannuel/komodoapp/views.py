from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import VmDeployForm
from .models import Vm_Info, Users
import requests, json, time
from .api import WorkflowManager
# Create your views here.

@login_required
def index(request):
    current_user = request.user
    return render(request,"index.html", { 'username': current_user } )

def login(request):
    if request.method == "POST" :
      save_current_user(request.user)
    return redirect('/accounts/login')

def logout(request):
    return redirect('/accounts/logout')

@login_required
def vm_deploy(request):
    current_user = request.user
    if request.method == "POST":
      spec_form = VmDeployForm(request.POST)
      if spec_form.is_valid():
        specs = spec_form.cleaned_data
        vm_create = WorkflowManager()
        current_user = str(request.user)
        trigger_api = WorkflowManager.trigger_workflow_vm(vm_create,specs, current_user)
        job_id = trigger_api['workflow_job']
        status = check_status(job_id)
        print('STATUS :', status)
        if 'successful' in status: 
          current_user = save_current_user(request.user)
          register_vm(specs, current_user, job_id)
          success = True 
          vm_hostname = specs['vm_name']
          return redirect('/portal/dashboard', {success: 'success', job_id : 'job_id', vm_hostname : 'vm_hostname'})
        else: 
          success = "Failed"
          return redirect('/portal/dashboard', {success: 'success', job_id : 'job_id', vm_hostname : 'vm_hostname'})
    else: 
      spec_form = VmDeployForm()
      
    return render(request,'vm_deploy.html', {'spec_form' : spec_form,'username': current_user})

@login_required
def dashboard(request):
    job_id = 0
    if request.method == "POST":
        user = request.user
        print('user: ',user)
        vm_hostname = request.POST.get('action')
        delete_guest = WorkflowManager()
        job_id = WorkflowManager.delete_vm(delete_guest, vm_hostname)
        status = check_status(job_id['workflow_job'])
        if 'successful' in status: 
           remove_vm = Vm_Info.objects.filter(vm_name = vm_hostname)
           print(remove_vm)
           remove_vm.delete()
           success = True
           return redirect('/portal/dashboard', {success: 'success', job_id['workflow_job']: 'job_id', vm_hostname : 'vm_hostname'})
        else:
           success = "Failed"
           return redirect('/portal/dashboard', {success: 'success', job_id['workflow_job'] : 'job_id', vm_hostname : 'vm_hostname'})
    vm_list = []
    current_user = request.user 
    user_vms = Vm_Info.objects.filter(user_id__in = Users.objects.filter(username=current_user))
    if user_vms: 
     for vm in user_vms : 
         vm = str(vm)
         vm = vm.replace('\'','')
         vm = vm.replace(' ','')
         vm = vm.split(',')
         vm_list.append(vm)
     print(vm_list)
    return render(request,'dashboard.html', {'user_vms' : vm_list , 'username': current_user})

def save_current_user(username):
        current_user = username
        user = Users()
        user.username = current_user 
        if not Users.objects.filter(username=current_user).exists():
          user.save()
          print('COUCOU')
        return current_user

def register_vm(specs, user, job_id): 
        vm_specs = Vm_Info(
        vm_name = specs['vm_name'],
        vm_memory = specs['vm_memory'],
        vm_cpus = specs['vm_cpus'],
        job = job_id,
        vm_disk_size = specs['vm_disk_size'],
        template = specs['template'],
        user_id = Users.objects.get(username=user))   

        vm_specs.save()

def check_status(job_id):
        
        check_stat = WorkflowManager()
        check = WorkflowManager.get_workflow_status(check_stat, job_id)
        print(check)
        while check['status'] not in ['successful', 'failed', 'canceled']:
           time.sleep(20)
           check = WorkflowManager.get_workflow_status(check_stat, job_id)
           print(check)
        if check['status'] in ['successful', 'failed', 'canceled']:
            return check['status']