from django.http import HttpRequest
import json 
from bookmyshow.common import response_sender,JWT,token_required
from http import HTTPStatus
from theatre_app.models import SeatModel,TheatreModel
from .models import TicketModel
from theatre_app.views import check_availability
from datetime import datetime,timedelta
from auth_app.models import Users,Activity
from django.db import transaction
from django.utils import timezone

@token_required()
def block_seat(user,request:HttpRequest,seat_id):
  
  print(timezone.now())
  if request.method == 'POST':
    with transaction.atomic():
      seat = SeatModel.objects.select_for_update().filter(id = seat_id).first()
      if seat is None:
        return response_sender(message='Invalid Seat Details',data=None,http=HTTPStatus.NOT_FOUND)
      status = check_availability(seat)
      if status == 'BLOCKED':
        return response_sender(message='Seat is Blocked',data=None,http=HTTPStatus.BAD_REQUEST)
      if status == 'BOOKED':
        return response_sender(message='Seat is Booked',data=None,http=HTTPStatus.BAD_REQUEST)
    
      seat.start_time = timezone.now()
      seat.end_time = timezone.now() + timedelta(minutes=10)
      seat.blocked_by = user
      seat.save()
    transaction.commit()
    return response_sender(message='Seat is blocked successfully',data=None,http=HTTPStatus.OK)
    
  else : 
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
@token_required()
def release_seat(user,request:HttpRequest,seat_id):
  if request.method == 'PUT':
    with transaction.atomic():
      seat = SeatModel.objects.select_for_update().filter(id = seat_id).first()
      if seat is None:
        return response_sender(message='Invalid Seat Details',data=None,http=HTTPStatus.NOT_FOUND)
      status = check_availability(seat)
      if status != 'BLOCKED':
        return response_sender(message='Invalid Action',data=None,http=HTTPStatus.BAD_REQUEST)
      if status == 'BOOKED':
        return response_sender(message='Seat is Booked',data=None,http=HTTPStatus.BAD_REQUEST)
    
      seat.start_time = timezone.now()
      seat.end_time = timezone.now() 
      seat.blocked_by = None
      seat.save()
    transaction.commit()
    return response_sender(message='Seat is Released successfully',data=None,http=HTTPStatus.OK)
    
  else : 
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
@token_required()
def book_seat(user,request:HttpRequest,seat_id):
  if request.method == 'PUT':
    with transaction.atomic():
      seat = SeatModel.objects.select_for_update().filter(id = seat_id).first()
      if seat is None:
        return response_sender(message='Invalid Seat Details',data=None,http=HTTPStatus.NOT_FOUND)
      status = check_availability(seat)
      if status != 'BLOCKED':
        return response_sender(message='Invalid Action',data=None,http=HTTPStatus.BAD_REQUEST)
      if status == 'AVAIL':
        return response_sender(message='Seat is not blocked',data=None,http=HTTPStatus.BAD_REQUEST)
      if seat.blocked_by != user:
        return response_sender(message='This seat is already booked by another person',data=None,http=HTTPStatus.BAD_REQUEST)
    
      ticket = TicketModel()
      ticket.user = user
      ticket.seat = seat
      ticket.save()
      seat.start_time = timezone.now()
      seat.end_time = timezone.now() 
      seat.blocked_by = None
      seat.save()
    transaction.commit()
    return response_sender(message='Seat is Released successfully',data=None,http=HTTPStatus.OK)
    
  else : 
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
