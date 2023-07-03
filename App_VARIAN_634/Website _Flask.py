from flask import Flask
from flask_socketio import SocketIO, emit
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import random

server = Flask(__name__)
app = Dash(__name__, server=server)
socketio = SocketIO(server)

# Create random data
data = {'values': [random.random() for _ in range(10)]}

app.layout = html.Div(
    children=[
        html.H1(children='Live Graph', style={'textAlign': 'center'}),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(id='graph-update', interval=1*1000)
    ]
)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph(n):
    global data
    data['values'].append(random.random())  # Add some new random data
    data['values'] = data['values'][-10:]  # Keep the last 10 data points

    trace = go.Scatter(
        y=data['values'],
        line=dict(color='rgba(10, 80, 0, .8)'),
        mode='lines+markers'
    )
    
    return {'data': [trace]}

if __name__ == '__main__':
    socketio.run(server, debug=True)
