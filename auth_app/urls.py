from django.urls import path
from . import views

urlpatterns = [
    path(route='signup',view=views.signup,name='signup'),
    path(route='login',view=views.login,name='login'),
    path(route='refresh',view=views.refresh,name='refresh'),
    path(route='logout',view=views.logout,name='logout')
]