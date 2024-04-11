from .models import Users

def get_current_user(email):

  return Users.objects.filter(email = email).first()