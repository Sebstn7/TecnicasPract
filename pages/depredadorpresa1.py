import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint

dash.register_page(__name__, path='/pagina9', name='Gilpin-Ayala',order=6)

layout = html.Div([
    html.Div([
        html.H2("Sistema Depredador-Presa Gilpin-Ayala", className="title"),

        html.Div([
            html.Label("Tasa intrínseca de crecimiento de la presa (r): "),
            dcc.Input(id='input-r', type='number', value=0.25, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Capacidad de carga ambiental de la presa (K): "),
            dcc.Input(id='input-K', type='number', value=10, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Exponente de Gilpin-Ayala (α): "),
            dcc.Input(id='input-alpha', type='number', value=0.5, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de captura del depredador (τ1): "),
            dcc.Input(id='input-tau1', type='number', value=0.33, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Coeficiente de conversión de presa a nuevos depredadores (τ2): "),
            dcc.Input(id='input-tau2', type='number', value=0.2, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Constante de semi-saturación (β): "),
            dcc.Input(id='input-beta', type='number', value=3.5, step=0.1, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tasa de mortalidad natural del depredador (ω): "),
            dcc.Input(id='input-omega', type='number', value=0.1, step=0.01, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Presas iniciales (A0): "),
            dcc.Input(id='input-A0', type='number', value=4, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Depredadores iniciales (B0): "),
            dcc.Input(id='input-B0', type='number', value=1, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Tiempo de simulación (días): "),
            dcc.Input(id='input-tiempo', type='number', value=250, className="input-field"),
        ], className="input-group"),

        html.Button("Simular Epidemia", id='btn-simular', className="btn-generar"),

    ],className="content left"),

    html.Div([
        html.H2("Evolución de las Poblaciones", className="title"),
        dcc.Graph(
            id='grafica-poblaciones-tiempo',
            style={'height':'450px','width':'100%'},
        ),
        dcc.Graph(
            id='grafica-presa-depredador',
            style={'height':'450px','width':'100%'},
        ),

    ], className="content right"),

],className="page-container")


def modelo_rumor(y, t, r, K, alpha, tau1, tau2, beta, omega):
    A, B  = y

    dA_dt = r*A*(1 - (A/K)**alpha) - tau1*(A**2/(A**2 + beta))*B
    dB_dt = (tau2*(A**2/(A**2 + beta)) - omega)*B      

    return [dA_dt, dB_dt]


@callback(
    Output('grafica-poblaciones-tiempo', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('input-r', 'value'),
    State('input-K', 'value'),
    State('input-alpha', 'value'),
    State('input-tau1', 'value'),
    State('input-tau2', 'value'),
    State('input-beta', 'value'),
    State('input-omega', 'value'),
    State('input-A0', 'value'),
    State('input-B0', 'value'),
    State('input-tiempo', 'value'),
    prevent_initial_call=False
)
def simular_poblaciones(n_clicks, r, K, alpha, tau1, tau2, beta, omega, A0, B0, tiempo_max):
    y0 = [A0, B0]

    t = np.linspace(0, tiempo_max, 200)

    try: 
        solucion = odeint(modelo_rumor, y0, t, args=(r, K, alpha, tau1, tau2, beta, omega))
        A,  B = solucion.T
    except Exception as e:
        A = np.full_like(t, A0)
        B = np.full_like(t, B0)
        
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=A, 
        mode='lines', 
        name='Presas (A)', 
        line=dict(color='blue', width=2),
        hovertemplate='Día %{x:.0f}<br>Presas: %{y:.2f}<extra></extra>'
        )
    )
    
    fig.add_trace(go.Scatter(
        x=t, y=B,
        mode='lines',
        name='Depredadores (B)',  
        line=dict(color='red', width=2),
        hovertemplate='Día %{x:.0f}<br>Depredadores: %{y:.2f}<extra></extra>'
        )
    )
    
    fig.update_layout(
        title=dict(
            text = "<b>Evolución de las Poblaciones</b>",
            x = 0.5, 
            font=dict(size=16, color='darkblue') 
        ),
        xaxis_title="tiempo (días)",
        yaxis_title="Número de animales (A, B)",
        paper_bgcolor='lightcyan',
        plot_bgcolor='white',
        font=dict(family='Outfit',size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=0.6
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )  

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    return fig


@callback(
    Output('grafica-presa-depredador', 'figure'),
    Input('btn-simular', 'n_clicks'),
    State('input-r', 'value'),
    State('input-K', 'value'),
    State('input-alpha', 'value'),
    State('input-tau1', 'value'),
    State('input-tau2', 'value'),
    State('input-beta', 'value'),
    State('input-omega', 'value'),
    State('input-A0', 'value'),
    State('input-B0', 'value'),
    State('input-tiempo', 'value'),
    prevent_initial_call=False
)

def simular_poblaciones2(n_clicks, r, K, alpha, tau1, tau2, beta, omega, A0, B0, tiempo_max):
    y0 = [A0, B0]

    t = np.linspace(0, tiempo_max, 200)

    try: 
        solucion = odeint(modelo_rumor, y0, t, args=(r, K, alpha, tau1, tau2, beta, omega))
        A,  B = solucion.T
    except Exception as e:
        A = np.full_like(t, A0)
        B = np.full_like(t, B0)
        
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=A, y=B,
        mode='lines',
        name='Todo (C)',  
        line=dict(color='green', width=2),
        hovertemplate='Presas %{x:.2f}<br>Depredadores: %{y:.2f}<extra></extra>'
        )
    )
    
    fig.update_layout(
        title=dict(
            text = "<b>Depredador vs Presa</b>",
            x = 0.5, 
            font=dict(size=16, color='darkblue') 
        ),
        xaxis_title="Número de presas (A)",
        yaxis_title="Número de depredadores (B)",
        paper_bgcolor='lightcyan',
        plot_bgcolor='white',
        font=dict(family='Outfit',size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.0,
            xanchor="right",
            x=0.6
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )  

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    return fig