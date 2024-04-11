from http import HTTPStatus
from django.http import JsonResponse
import bcrypt
import jwt
from datetime import datetime,timedelta,UTC
import uuid
from auth_app.models import Activity
from django.conf import settings


def response_sender(message,data,http:HTTPStatus):
  
  body = {
    'http_status':http.phrase,
    'message':message,
    'data':data
  }
  
  return JsonResponse(data = body,status = http.value)

def gethashpwd(pwd):
  
  return (bcrypt.hashpw(bytes(pwd,'utf-8'),bcrypt.gensalt(rounds=12))).decode('utf-8')


def checkpwd(pwd:str,hpwd:str):
  
  return bcrypt.checkpw(hashed_password=hpwd.encode('utf-8'),password=pwd.encode('utf-8'))



class JWT:
  
  
  def get_jwt(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(settings.JWT_TOKEN_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    
    if payload is None : 
      payload = jwt_claims
    
    payload.update(jwt_claims)
    
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGO)
  
  
  def get_jwt_refresh(subject,payload = None):
    
    jwt_claims = {
      'exp' : datetime.now(UTC) + timedelta(seconds=float(settings.JWT_REFRESH_TIME)),
      'sub' : subject,
      'iat' : datetime.now(UTC)
    }
    
    if payload is None : 
      payload = jwt_claims
      
    payload.update(jwt_claims)
    
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGO)
  
  def verify_jwt_token(token):
    try:
      payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGO],verify=True)
      return payload  
    except jwt.ExpiredSignatureError as e:
      return None
    except jwt.InvalidTokenError as e:
      return None
    except Exception as e:
      return None
    
def get_random_id():
    return uuid.uuid4().hex
  
  
def token_required():
  def wrapper(func):
    def wrapper_func(request,*args,**kwargs):
      if 'Authorization' not in request.headers:
        return response_sender(message='Make Login First',data=None,http=HTTPStatus.FORBIDDEN)
      jwt_details = JWT.verify_jwt_token(request.headers['Authorization'])
      if jwt_details is None:
        return response_sender(message='Make Login First',data=None,http=HTTPStatus.FORBIDDEN)
      session_id  = jwt_details['sub']
      if session_id is None:
        return response_sender(message='Make Login First',data=None,http=HTTPStatus.FORBIDDEN)
      activity = Activity.objects.filter(session_id = session_id).first()
      if activity is None:
        return response_sender(message='Make Login First',data=None,http=HTTPStatus.FORBIDDEN)
      return func(activity.user,request,*args, **kwargs)
    return wrapper_func
  return wrapper