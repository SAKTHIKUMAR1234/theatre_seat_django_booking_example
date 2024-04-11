from django.db import models


class Base(models.Model):
  
  id = models.AutoField(primary_key=True)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  class Meta:
    
    abstract = True
    
    
class Users(Base):
  
  name = models.CharField(max_length = 100 ,null = False,blank = False)
  email = models.EmailField()
  password = models.TextField()
  isdev = models.BooleanField(default = False)
  

class Activity(Base):
  
  session_id = models.CharField(max_length = 60,null = False,blank = False)
  login_at = models.DateTimeField(auto_now_add = True)
  logout_at = models.DateTimeField(null = True,blank = True)
  user = models.ForeignKey(Users,on_delete = models.CASCADE,related_name = 'sessions')