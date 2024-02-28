from django.urls import path
from .views import get_curs


urlpatterns = [
    path('valute/<str:pk>', get_curs, name="get_curs"),
]