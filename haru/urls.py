from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views





app_name = 'haru'

urlpatterns = [

    # path('', first, name="first"),

    # path('trading/', views.home, name="home"),
    # path('', views.first, name="first"),
]

#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)