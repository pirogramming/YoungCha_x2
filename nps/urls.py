from django.urls import path

from nps import views

app_name = 'nps'

urlpatterns = [
    path('debug', views.home, name='crawling'),
    path('', views.home2, name='nps'),
]