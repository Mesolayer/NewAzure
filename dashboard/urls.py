from django.urls import path
from . import views

# urls for dashboard pages
urlpatterns = [

    path('', views.dashboard, name='dashboard'),
]
