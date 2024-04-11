from django.urls import path
from . import views

urlpatterns = [
  path('create',view=views.create_theatre,name='create_theatre'),
  path('get/all',view=views.get_all_theatre,name='get_all_theatre'),
  path('get/<int:id>',view=views.get_theatre_seating_details,name='threatre_details_by_id')
]