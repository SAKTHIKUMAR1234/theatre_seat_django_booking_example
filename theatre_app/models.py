import datetime

from django.db import models
from auth_app.models import Base, Users


class TheatreModel(Base):
    name = models.CharField(max_length=150)


class SeatModel(Base):
    theatre = models.ForeignKey(TheatreModel, on_delete=models.CASCADE, related_name='seats')
    seat_no = models.CharField(max_length=3)
    row_no = models.IntegerField()
    column_no = models.IntegerField()
    start_time = models.DateTimeField(default=None, null=True)
    end_time = models.DateTimeField(default=None, null=True)
    blocked_by = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, default=None)
