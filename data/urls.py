from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='data'

urlpatterns = [
    # path('home/<str:name>/', views.data_show),
    path('ing/', views.data_show),
    path('result/', views.user_result, name = 'result'),
    # path('', views.loading, ),
    path('leaderboard/', views.leader_board, name='leader_board'),
    path('ready', views.ready, name ='data_home'),
    path('', views.index, name="index"),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)