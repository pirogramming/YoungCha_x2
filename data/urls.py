from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name='data'

urlpatterns = [
    # path('home/<str:name>/', views.data_show),
    path('home/ing/', views.data_show),
    path('home/result', views.user_result, name = 'result'),
    # path('', views.loading, ),
    path('home/', views.home, name ='data_home'),
    path('readerboard/', views.reader_board, name='reader_board')

]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)