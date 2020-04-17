#!/usr/bin/env python

import os

import pandas as PD
import plotly.graph_objects as GO

import dash  
import dash_core_components as DCC 
import dash_html_components as HTML  

v_val  = ['Fxx' , 'Fxx' , 'Cx' , 'Pxx']
m_val  = ['aaa' , 'bbb' , 'ccc' , 'eee']
tput_val  = [25000000 , 30000000 , 74000000 , 10000000]
smax_val = [25 , 30 , 74 , 100]

graph_dict = {'Vender' : v_val , 'Model' : m_val , 'Throughput(bps)' : tput_val , 'Session MAX' : smax_val}
df = PD.DataFrame.from_dict(graph_dict)

op_list = []
all_list = []
all_dict = {'label': 'ALL', 'value': 'ALL'}
op_tuple = [{'label': i, 'value': i} for i in df['Vender'].value_counts().index.tolist()], # ユニーク値をタプル化
count_list = [{'label': 'Throughput(bps)', 'value': 'Throughput(bps)'} , {'label': 'Session MAX', 'value': 'Session MAX'}]

for t in op_tuple:
    for l in t:
        op_list.append(l)
        all_list.append(l['value'])

op_list.append(all_dict)

ex_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__ , external_stylesheets = ex_stylesheets)

server = app.server # heroku Up用

app.layout = HTML.Div(
    HTML.Div([
        HTML.Div([
            HTML.H5('型番'),
            DCC.Dropdown(
                id = "dd_model",
                options = op_list,
                value = 'ALL'
                ),
            ]),
            
        HTML.Div([
            HTML.H5('スペック'),
            DCC.Dropdown(
                id = "dd_count",
                options = count_list,
                value = 'Throughput(bps)'
                ),
            ]),

    DCC.Graph(
        id = "graph"
        )
    ])
)

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dd_model', 'value'),
    dash.dependencies.Input('dd_count', 'value')]
)

def update_graph(model_id , count_id):
    if ( model_id == 'ALL' ):
        factor_list = all_list
    else:
        factor_list = ['{}'.format(model_id)]

    dff = df[df['Vender'].isin(factor_list)]

    return{
        'data' : [
            GO.Bar( # 棒グラフ
                x = dff['Model'],
                y = dff[count_id],
                name = count_id,
            )
        ],
        'layout' : {
            'xaxis' : {'title' : '型番'},
            'yaxis' : {'title' : '{}'.format(count_id)},
        }
    }

if __name__ == '__main__': # スクリプトを直接実行時は__name__に__main__が自動で入る
    app.run_server(debug = True)


