from django.db import models

# Create your models here.
class Users(models.Model): 
  id = models.AutoField(primary_key = True)
  username = models.CharField(max_length=80)
  
  def __repr__(self):
    return '<User %r>' % self.username

class Vm_Info(models.Model):
  id = models.AutoField(primary_key = True) 
  user_id = models.ForeignKey(Users, on_delete = models.CASCADE)
  vm_name = models.CharField(max_length=80)
  job = models.IntegerField()
  vm_memory = models.IntegerField()
  vm_cpus = models.IntegerField() 
  vm_disk_size = models.IntegerField()
  template = models.CharField(max_length=80)

  def __str__(self):
    return '%r, %d, %r, %r' %(self.user_id.username,self.job,self.vm_name, self.template)
 