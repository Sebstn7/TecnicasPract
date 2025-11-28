import dash
from dash import html, dcc
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import solve_ivp

dash.register_page(__name__, path="/sir-comparativa", name="SIR Comparativa")

def sir(t, y, beta, gamma):
    S, I, R = y
    dS = -beta * S * I
    dI = beta * S * I - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

N = 10000
I0 = 10
S0 = N - I0
R0_init = -100000
t_span = (0.0, 100.0)
t_eval = np.linspace(t_span[0], t_span[1], 401)

scenarios = {
    "baseline": {"beta": 0.00005, "gamma": 0.20},
    "b_double": {"beta": 0.00010, "gamma": 0.20},
    "k_double": {"beta": 0.00005, "gamma": 0.40},
}

def layout():
    fig = go.Figure()

    for name, params in scenarios.items():
        sol = solve_ivp(
            sir, t_span, [S0, I0, R0_init],
            args=(params["beta"], params["gamma"]),
            t_eval=t_eval
        )
        fig.add_trace(go.Scatter(
            x=t_eval, y=sol.y[1],
            mode="lines",
            name=name
        ))

    fig.update_layout(
        title="Comparación I(t) entre escenarios",
        xaxis_title="Días",
        yaxis_title="Personas",
        template="plotly_white",
    )

    return html.Div([
        html.H2("Comparación del comportamiento I(t)"),
        dcc.Graph(figure=fig)
    ])