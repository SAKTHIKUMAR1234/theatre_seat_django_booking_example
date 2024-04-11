from django.http import HttpRequest
from http import HTTPStatus
from bookmyshow.common import response_sender,checkpwd,gethashpwd,get_random_id,JWT
import json
from .serializers import SignupSerializer,LoginSerializer
from .models import Users,Activity
from django.db import transaction
from django.utils import timezone


def signup(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      signup_data = SignupSerializer(data=json_data)
      if not signup_data.is_valid() :
        return response_sender(message='Invalid Data',data=None,http=HTTPStatus.BAD_REQUEST)
      signup_data = signup_data.data
      exist = Users.objects.filter(email = signup_data['email']).first()
      if exist is not None:
        return response_sender(message='email already exist',data={'email':signup_data['email']},http=HTTPStatus.CONFLICT)
      with transaction.atomic():
        user = Users()
        user.name = signup_data['name']
        user.email = signup_data['email']
        user.password = gethashpwd(pwd = signup_data['password'])
        user.save()
      transaction.commit()
      return response_sender(message='user created successfully',data=None,http=HTTPStatus.CREATED)
    except json.JSONDecodeError :
      transaction.rollback()
      return response_sender(message='Invalid Data',data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      transaction.rollback()
      return response_sender(message='OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else : 
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  

def login(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      login_data = LoginSerializer(data=json_data)
      if not login_data.is_valid() :
        return response_sender(message='Invalid Data',data=None,http=HTTPStatus.BAD_REQUEST)
      login_data = login_data.data
      user = Users.objects.filter(email = login_data['email']).first()
      if user is None:
        return response_sender(message='The given email not found',data={'email':login_data['email']},http=HTTPStatus.NOT_FOUND)
      
      if not checkpwd(pwd = login_data['password'],hpwd=user.password) :
        return response_sender(message='Incorrect credentials',data=None,http=HTTPStatus.FORBIDDEN)
      with transaction.atomic():
        activity = Activity()
        activity.session_id = get_random_id()
        activity.user = user
        activity.save()
        tokens = {
          'auth_token' : JWT.get_jwt(subject=activity.session_id),
          'refresh_token' : JWT.get_jwt_refresh(subject=activity.session_id)
        }
      transaction.commit()
      return response_sender(message='logged in successfully',data = tokens,http=HTTPStatus.OK)
    except json.JSONDecodeError :
      transaction.rollback()
      return response_sender(message='Invalid Data',data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      transaction.rollback()
      return response_sender(message='OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else : 
    return response_sender(message='invalid request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
def logout(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      session_id = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
      session = Activity.objects.filter(session_id = session_id).first()
      if session == None or session.logout_at != None:
        return response_sender(message='Frobidden',data=None,http=HTTPStatus.FORBIDDEN)
      session.logout_at = timezone.now()
      session.save()
      return response_sender(message='logged out successfully',data=None,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message='OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
def refresh(request:HttpRequest):
  
  if request.method == 'GET':
    try:
      claim = {
        'is_extended':'True'
      }
      session_id  = JWT.verify_jwt_token(request.headers['Authorization'])['sub']
      token = JWT.get_jwt(session_id,claim)
      ref_token = JWT.get_jwt_refresh(session_id,claim)
      
      token_response = {
        'token':token ,
        'refresh_token':ref_token
      }
      return response_sender(message='refresh token generated',data=token_response,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message='OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  