from django.db import models
from auth_app.models import Base,Users
from theatre_app.models import SeatModel


class TicketModel(Base):
  
  seat = models.ForeignKey(SeatModel,on_delete=models.DO_NOTHING,related_name='booking')
  user = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name='bookings')
