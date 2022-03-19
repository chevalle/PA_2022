from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import VmDeployForm
from .models import Vm_Info, Users
import requests, json
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
    
    if request.method == "POST":
      spec_form = VmDeployForm(request.POST)
      if spec_form.is_valid():
        specs = spec_form.cleaned_data
        vm_create = WorkflowManager()
        current_user = str(request.user)
        trigger_api = WorkflowManager.trigger_workflow_vm(vm_create,specs, current_user)
        job_id = trigger_api['workflow_job']
        current_user = save_current_user(request.user)
        register_vm(specs, current_user, job_id)
    else: 
      spec_form = VmDeployForm()
      
    return render(request,'vm_deploy.html', {'spec_form' : spec_form})

@login_required
def dashboard(request):
    
    current_user = request.user 
    user_vms = Vm_Info.objects.filter(user_id__in = Users.objects.filter(username=current_user))
    print(user_vms)
    return render(request,'dashboard.html', {'user_vms' : user_vms})

def save_current_user(username):
        current_user = username
        user = Users()
        user.username = current_user 
        if not Users.objects.filter(username=current_user).exists():
          user.save()
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
