from django.urls import path
from . import views

urlpatterns = [
  path('block/<int:seat_id>',view=views.block_seat,name='block_seat'),
  path('release/<int:seat_id>',view=views.release_seat,name='release_seat'),
  path('book/<int:seat_id>',view=views.book_seat,name='book_seat')
]