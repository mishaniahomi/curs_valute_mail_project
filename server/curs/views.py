from django.shortcuts import render
import datetime
import plotly.express as px
import dash_bootstrap_components as dbc


from .models import Curs, Valute
from .forms import DateForm



def get_curs(request, pk):
    external_stylesheets = [dbc.themes.CERULEAN]
    start = request.GET.get('start')
    end = request.GET.get('end')

    
    val = Valute.objects.get(pk=pk)
    
    curs2 = Curs.objects.filter(valute_id=val).order_by('datetime')
    if start:
        curs2 = curs2.filter(datetime__gte=start)
    if end:
        curs2 = curs2.filter(datetime__lte=end)


    fig = px.line(
        x = [c.datetime for c in curs2],
        y = [c.value for c in curs2],
        title ="График изменений курса",
        labels={'x':'Дата', 'y':'Курс'},
    )
    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })
    chart = fig.to_html()
    return render(request, 'curs/get_valute.html', context={'val': val, 'chart':chart, 'form': DateForm() })
