from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Users, Vm_Info

class VmDeployForm(forms.Form):

    vm_name = forms.CharField(
        label = "VM Hostname",
        max_length = 80,
        required = True,
    )

    vm_memory = forms.ChoiceField(
        label = 'VM Memory',
        required = True,
        choices=[
            ('512', '512 Mb'),
            ('1024', '1 Gb'),
            ('2048', '2 Gb')
        ]
    )
    vm_cpus = forms.ChoiceField(
        label = 'VM CPUs',
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
        label = 'Disk Size',
        required = True,
        choices=[
            ('15', '15 GB'),
            ('20', '20 GB'),
            ('25', '25 GB'),
            ('30', '30 GB'),
        ]
    )

    template = forms.ChoiceField(
        label = 'Template',
        required = True,
        choices=[
            ('Template-DEB10', 'Debian 10'),
        ]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-vmdeployForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-vmdeployForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Submit'))