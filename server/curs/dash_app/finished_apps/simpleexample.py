import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from curs.models import Curs, Valute

external_stylesheets = [dbc.themes.CERULEAN]

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


app.layout = html.Div([
     dcc.Dropdown(
        pd.DataFrame(list(Valute.objects.all().values()))['name'],   
        'Австралийский доллар',    
        id='shoose_valute',

    ),
    html.Div(id='valute_name'),
    html.H1('График изменений курса'),
    dcc.Graph(id='slider-graph', animate=False, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
 
])

@app.callback(
            Output('valute_name', 'children'),
            [Input('shoose_valute', 'value')]
              )
def get_and_set_valute_name(value):
    valute = Valute.objects.get(name=value)
    return html.Div([
            html.H1(value),
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P('Обозначение'),
                                    ], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                                    html.Div([
                                        html.P(valute.unique_id),
                                    ], className="h5 mb-0 font-weight-bold text-gray-800"),
                                ], className="col mr-2"),
                            ], className="row no-gutters align-items-center"),
                        ], className="card-body"),
                    ], className="card border-left-primary shadow h-100 py-2"),
                ], className="col-xl-3 col-md-6 mb-4"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P('ЧИСЛОВОЙ КОД'),
                                    ], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                                    html.Div([
                                        html.P(valute.num_code),
                                    ], className="h5 mb-0 font-weight-bold text-gray-800"),
                                ], className="col mr-2"),
                            ], className="row no-gutters align-items-center"),
                        ], className="card-body"),
                    ], className="card border-left-primary shadow h-100 py-2"),
                ], className="col-xl-3 col-md-6 mb-4"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P('БУКВЕННЫЙ КОД'),
                                    ], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                                    html.Div([
                                        html.P(valute.char_code),
                                    ], className="h5 mb-0 font-weight-bold text-gray-800"),
                                ], className="col mr-2"),
                            ], className="row no-gutters align-items-center"),
                        ], className="card-body"),
                    ], className="card border-left-primary shadow h-100 py-2"),
                ], className="col-xl-3 col-md-6 mb-4"),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Div([
                                        html.P('НОМИНАЛ'),
                                    ], className="text-xs font-weight-bold text-primary text-uppercase mb-1"),
                                    html.Div([
                                        html.P(valute.nominal),
                                    ], className="h5 mb-0 font-weight-bold text-gray-800"),
                                ], className="col mr-2"),
                            ], className="row no-gutters align-items-center"),
                        ], className="card-body"),
                    ], className="card border-left-primary shadow h-100 py-2"),
                ], className="col-xl-3 col-md-6 mb-4"),
            ], className="row"),
           ])


@app.callback(
            Output('slider-graph', 'figure'),
            [Input('shoose_valute', 'value')]
              )
def display_value(value):

    valute = Valute.objects.get(name=value)
    curs_data = Curs.objects.filter(valute_id=valute).order_by('datetime')
    
    x = [c.datetime for c in curs_data],
    y = [c.value for c in curs_data],
    

    graph = go.Scatter(
        x = [c.datetime for c in curs_data],
        y = [c.value for c in curs_data],
        name='Manipulate Graph'
    )
    layout = go.Layout(
        # paper_bgcolor='rgba(255,255,255,255)',
        # plot_bgcolor='rgba(255,255,255,255)',
        # xaxis=dict(range=[min(x), max(x)]),
        # yaxis=dict(range=[min(y), max(y)]),
        # font=dict(color='black'),

    )
    return {'data': [graph], 'layout': layout}