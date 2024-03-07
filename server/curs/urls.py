from django.urls import path
from .views import get_curs
from curs.dash_app.finished_apps import simpleexample

urlpatterns = [
    path('valute', get_curs, name="get_curs"),
]