from django.http import HttpRequest
import json 
from bookmyshow.common import response_sender
from http import HTTPStatus
from .serializers import TheatreSerializer
from .models import TheatreModel,SeatModel
from django.db import transaction
from datetime import datetime
from django.utils import timezone

def check_availability(seat):
  current_datetime = timezone.now()
  
  if seat.booking.first() : 
    return 'BOOKED'
  elif (seat.start_time == None or seat.end_time == None) :
    return 'AVAIL'
  elif  (seat.end_time >= current_datetime and seat.blocked_by is not None):
    return 'BLOCKED'
  else:
    return 'AVAIL'

def create_theatre(request:HttpRequest):
  
  if request.method == 'POST':
    try:
      json_data = json.loads(request.body)
      theatreserializer = TheatreSerializer(data=json_data)
      if not theatreserializer.is_valid():
        return response_sender(message = theatreserializer.errors,data=None,http=HTTPStatus.BAD_REQUEST)
      else:
        theatre_name = theatreserializer.validated_data['theatre_name']
        seat_layout = theatreserializer.validated_data['seat_layout']
        with transaction.atomic():
          theatre = TheatreModel()
          theatre.name = theatre_name
          theatre.save()
          for row_idx, row in enumerate(seat_layout):
              for seat_idx, seat_no in enumerate(row):
                  seat = SeatModel()
                  seat.seat_no = seat_no
                  seat.column_no = seat_idx
                  seat.row_no = row_idx
                  seat.theatre = theatre
                  seat.save()
        transaction.commit()
        return response_sender('Theatre Created Successfully',data=None,http=HTTPStatus.CREATED)
    except json.JSONDecodeError as e:
      return response_sender(message = 'Invalid Data',data=None,http=HTTPStatus.BAD_REQUEST)
    except Exception as e:
      print(e)
      transaction.rollback()
      return response_sender(message = 'OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
  
def get_all_theatre(request : HttpRequest):
  
  if request.method == 'GET':
    try:
      theatres_list = TheatreModel.objects.all()
      response_body = [
        {
          'theatre_name':theatre.name,
          'theatre_id' : theatre.id
        }
        for theatre in theatres_list
      ]
      return response_sender('Theatre\'s fetched',data=response_body,http=HTTPStatus.OK)
    except Exception as e:
      return response_sender(message = 'OOPS something went wrong',data=None,http=HTTPStatus.INTERNAL_SERVER_ERROR)
  else:
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
    
    
def get_theatre_seating_details(request:HttpRequest,id:int):
  
  if request.method == 'GET':
    
    theatre = TheatreModel.objects.filter(id = id).first()
    if theatre is None:
      return response_sender(message='given theatre not found',data=None,http=HTTPStatus.NOT_FOUND)
    seats = theatre.seats.all().order_by('created_at')
    max_row = max(seats.values_list('row_no', flat=True)) + 1
    max_col = max(seats.values_list('column_no', flat=True)) + 1
    seating_layout = [['' for _ in range(max_col)] for _ in range(max_row)]
    for seat in seats:
        seating_layout[seat.row_no][seat.column_no] = {
          'seat_id' : seat.id,
          'seat_no' : seat.seat_no,
          'is_available' : check_availability(seat)
        }
    
    response_body = {
        'theatre_name': theatre.name,
        'seating_layout': seating_layout
    }
    return response_sender(message=id,data=response_body,http=HTTPStatus.OK)
  else:
    return response_sender(message='Invalid Request',data=None,http=HTTPStatus.BAD_GATEWAY)
  
