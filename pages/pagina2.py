import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np


t = np.linspace(0, 50, 20)  
K = 1000
P0 = 100
r = 0.3

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
    name='P(t) = K / (1 + ((K - P0)/P0)e^(-rt))',
    hovertemplate='t: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
)

fig = go.Figure(data=trace)

fig.update_layout(
    title=dict(
        text='<b>Capacidad de carga</b>',
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



dash.register_page(__name__, path='/pagina2', name='Pagina 2', order=3)

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Capacidad de carga", className="title"),

        dcc.Markdown("""
        En la naturaleza los recursos son limitados, entonces el crecimiento exponencial no puede seguir para siempre.
        El modelo logístico es más realista porque incluye una capacidad de carga máxima $K$ que representa el límite
        de individuos que el ambiente puede soportar.
        """, mathjax=True),

        dcc.Markdown("""
        La ecuación diferencial del modelo es:

        $$\\frac{dP}{dt} = rP \\left(1 - \\frac{P}{K}\\right)$$

        Donde el término $\\left(1 - \\frac{P}{K}\\right)$ actúa como freno cuando la población se acerca a $K$.
        """, mathjax=True),

        dcc.Markdown("""
        Resolviendo la ecuación obtenemos la función logística:

        $$P(t) = \\frac{K}{1 + \\left(\\frac{K - P_0}{P_0}\\right)e^{-rt}}$$

        En la gráfica vemos como la población crece rápido al principio pero después se va haciendo más lenta
        hasta que se estabiliza en $K = 1000$. Usamos $P_0 = 100$ y $r = 0.3$.
        """, mathjax=True),
    ], className="content left"),

    html.Div(children=[
        html.H2("Gráfica", className="title"),

        dcc.Graph(
            figure=fig,
            style={'height': '350px', 'width': '100%'},
        )
    ], className="content right")
], className="page-container")