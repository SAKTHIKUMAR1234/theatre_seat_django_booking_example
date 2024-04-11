

from typing import Any
from django.http import HttpRequest,HttpResponse, JsonResponse
import os
from django.conf import settings
import logging
from datetime import date,datetime

class LoggingMiddleware:
  
  def __init__(self,get_response) -> None:
    self.get_response = get_response
    
  def __call__(self, request:HttpRequest) -> Any:
    base_path = settings.BASE_DIR
    if not os.path.exists(os.path.join(base_path,'logs')):
      os.mkdir(os.path.join(base_path,'logs'))
    base_path = os.path.join(base_path,'logs')
    today = date.today()
    if not os.path.exists(os.path.join(base_path,str(today))):
      os.mkdir(os.path.join(base_path,str(today)))
    base_path = os.path.join(base_path,str(today))
    response:HttpResponse =  self.get_response(request)
    logging.basicConfig(filename=os.path.join(base_path,'mainlog.log'), level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    if response.status_code == 200:
      logger.info(f'{datetime.now()} is success response sended for path {request.path}')
    else :
      logger.error(f'{datetime.now()} is success response sended for path {request.path} due to the response body is {str(response.content)}')
    return response
  
def custome_logger(user,response:JsonResponse):
  
  base_path = settings.BASE_DIR
  if not os.path.exists(os.path.join(base_path,'logs')):
    os.mkdir(os.path.join(base_path,'logs'))
  base_path = os.path.join(base_path,'logs')
  today = date.today()
  if not os.path.exists(os.path.join(base_path,str(today))):
    os.mkdir(os.path.join(base_path,str(today)))
  base_path = os.path.join(base_path,str(today))
  logging.basicConfig(filename=os.path.join(base_path,str(f'{user.email}.log')),level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
  logger = logging.getLogger()
  logger.info(str(response.content))
  
    