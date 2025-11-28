import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output, State

dash.register_page(__name__, path='/pagina3', name='Pagina 3',order=4)

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Parámetros del Modelo", className="title"),
        
        html.Div([
            html.Label("Población Inicial (P0)", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
            dcc.Input(
                id='poblacion-inicial',
                type='number',
                value=100,
                style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
            ),
            
            html.Label("Capacidad de Carga (K)", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
            dcc.Input(
                id='capacidad-carga',
                type='number',
                value=1000,
                style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
            ),
            
            html.Label("Tasa de Crecimiento (r)", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
            dcc.Input(
                id='tasa-crecimiento',
                type='number',
                value=0.3,
                step=0.1,
                style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
            ),
            
            html.Label("Tiempo Máximo", style={'marginBottom': '5px', 'fontWeight': 'bold'}),
            dcc.Input(
                id='tiempo-maximo',
                type='number',
                value=50,
                style={'width': '100%', 'padding': '8px', 'marginBottom': '20px'}
            ),
            
            html.Button(
                'Generar Gráfica',
                id='generar-grafica',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'backgroundColor': '#1e3a5f',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'fontSize': '16px',
                    'cursor': 'pointer'
                }
            )
        ], style={'padding': '20px'})
    ], className="content left"),

    html.Div(children=[
        html.H2("Gráfica", className="title"),
        dcc.Graph(
            id='grafica-interactiva',
            style={'height': '350px', 'width': '100%'},
        )
    ], className="content right")
], className="page-container")

@dash.callback(
    Output('grafica-interactiva', 'figure'),
    Input('generar-grafica', 'n_clicks'),
    State('poblacion-inicial', 'value'),
    State('capacidad-carga', 'value'),
    State('tasa-crecimiento', 'value'),
    State('tiempo-maximo', 'value')
)
def actualizar_grafica(n_clicks, P0, K, r, t_max):
    if n_clicks is None:
        t = np.linspace(0, 50, 20)
        P0 = 100
        K = 1000
        r = 0.3
        P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))
    else:
        t = np.linspace(0, t_max, 50)
        P = K / (1 + ((K - P0) / P0) * np.exp(-r * t))
    
    trace = go.Scatter(
        x=t,
        y=P,
        mode='lines+markers',
        line=dict(
            dash='dot',
            color='black',
            width=2
        ),
        marker=dict(
            color='blue',
            symbol='square',
            size=8
        ),
        name=f'P(t) = {K} / (1 + (({K} - {P0})/{P0})e^(-{r}t))',
        hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
    )
    
    fig = go.Figure(data=trace)
    
    fig.update_layout(
        title=dict(
            text='<b>Modelo Logístico Interactivo</b>',
            font=dict(
                size=20,
                color='green'
            ),
            x=0.5,
            y=0.93
        ),
        xaxis_title='Tiempo (t)',
        yaxis_title='Población P(t)',
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor='lightblue',
        plot_bgcolor='white',
        font=dict(
            family='Outfit',
            size=11,
            color='black'
        )
    )
    
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink',
        zeroline=True, zerolinewidth=2, zerolinecolor='red',
        showline=True, linecolor='black', linewidth=2, mirror=True,
    )
    
    return fig