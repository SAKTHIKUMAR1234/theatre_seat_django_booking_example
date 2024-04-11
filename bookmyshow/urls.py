
from django.urls import path,include


urlpatterns = [
  path('api/theatre/',include('theatre_app.urls')),
  path('api/auth/',include('auth_app.urls')),
  path('api/book/',include('book_app.urls'))
]
