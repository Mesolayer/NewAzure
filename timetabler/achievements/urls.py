from django.urls import path
from .import views

urlpatterns = [
    path('', views.achievements, name='achievements'),

    #path('login/', include('login.urls')),
]
