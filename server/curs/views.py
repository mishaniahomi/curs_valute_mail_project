from django.shortcuts import render
from .models import Curs, Valute
import datetime

def get_curs(request, pk):
    days = 99999
    allow_days = [7,30,365,99999]
    val = Valute.objects.get(pk=pk)
    if request.GET.getlist('filter_search'):
        days = int(request.GET['filter_search'])
        curs = Curs.objects.filter(valute_id=val, datetime__gte=datetime.datetime.now()-datetime.timedelta(days)).order_by('datetime')
    else:
        curs = Curs.objects.filter(valute_id=val).order_by('datetime')
    return render(request, 'curs/get_valute.html', context={'val': val, 'curs': curs, 'days': days, 'allow_days':allow_days})
