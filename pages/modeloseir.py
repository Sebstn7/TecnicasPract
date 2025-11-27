import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint

dash.register_page(__name__, path='/pagina7', name='Modelo SEIR')

layout = html.Div([
    html.Div([
        html.H2("Modelo SEIR - Epidemiología", className="title"),

        html.Div([
            html.Label("Población Total (N):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-N', type='number', value=1000, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de transmisión (β):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-beta', type='number', value=0.5, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de incubación (σ):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-sigma', type='number', value=0.2, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de recuperación (γ):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-gamma', type='number', value=0.1, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Infectados iniciales (I0):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-I0', type='number', value=1, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo de simulación (días):", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-tiempo', type='number', value=100, className="input-field"),
        ], className="input-group"),

        html.Button("Generar gráfica", id='btn-simular', className="btn-generar"),

    ], className="content left"),

    html.Div([
        html.H2("Gráfica", className="title"),

        html.Div(
            dcc.Graph(
                id='grafica-seir',
                style={'height': '420px', 'width': '100%'}
            ),
            
        )

    ], className="content right"),

], className="page-container")


def modelo_seir(y, t, beta, sigma, gamma, N):
    S, E, I, R = y
    dS_dt = -beta * S * I / N
    dE_dt = beta * S * I / N - sigma * E
    dI_dt = sigma * E - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dE_dt, dI_dt, dR_dt]


@callback(
    Output('grafica-seir', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('input-N', 'value'),
    State('input-beta', 'value'),
    State('input-sigma', 'value'),
    State('input-gamma', 'value'),
    State('input-I0', 'value'),
    State('input-tiempo', 'value'),
    prevent_initial_call=False
)
def simular_seir(n_clicks, N, beta, sigma, gamma, I0, tiempo_max):
    S0 = N - I0
    y0 = [S0, 0, I0, 0]
    t = np.linspace(0, tiempo_max, 200)

    try:
        solucion = odeint(modelo_seir, y0, t, args=(beta, sigma, gamma, N))
        S, E, I, R = solucion.T
    except:
        S = np.full_like(t, S0)
        E = np.full_like(t, 0)
        I = np.full_like(t, I0)
        R = np.full_like(t, 0)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=t, y=S, mode='lines', name='Susceptibles (S)', line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=t, y=E, mode='lines', name='Expuestos (E)', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=t, y=I, mode='lines', name='Infectados (I)', line=dict(color='red', width=2)))
    fig.add_trace(go.Scatter(x=t, y=R, mode='lines', name='Recuperados (R)', line=dict(color='green', width=2)))

    fig.update_layout(
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de personas",
        paper_bgcolor='lightblue',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=12, color='black'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=0.5),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        showline=True, linecolor='black', linewidth=2, mirror=True
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        showline=True, linecolor='black', linewidth=2, mirror=True
    )

    return fig
