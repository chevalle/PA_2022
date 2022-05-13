from django import forms
from .models import Users, Vm_Info
from material import *

class VmDeployForm(forms.Form):

    vm_name = forms.CharField(required = True)

    vm_memory = forms.ChoiceField(
        
        required = True,
        choices=(
            ('512', '512 Mb'),
            ('1024', '1 Gb'),
            ('2048', '2 Gb')
       )
    )
    vm_cpus = forms.ChoiceField(
        
        required = True,
        choices=[
            ('1', '1'),
            ('2', '2')
        ]
    )
#    vm_cpu_cores = forms.ChoiceField(
 #       label = 'CPU Cores',
 #       required = True,
 #       choices=[
 #           ('1', '1'),
##            ('2', '2')
#        ]"""
#    )
    vm_disk_size = forms.ChoiceField(
        
        required = True,
        choices=[
            ('15', '15 GB'),
            ('20', '20 GB'),
            ('25', '25 GB'),
            ('30', '30 GB'),
        ]
    )

    template = forms.ChoiceField(
    
        required = True,
        choices=[
            ('Template-DEB10', 'Debian 10'),
            ('Template-CENTOS7', 'CentOS 7')
        ]
    )

class UserLogin(forms.Form):
   
    username = forms.CharField(
        label = 'Username',
        required= True,
    )

    password = forms.CharField(
        label = 'Password',
        required= True,
        widget = forms.PasswordInput(),
    )

    