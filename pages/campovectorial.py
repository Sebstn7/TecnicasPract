import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objs as go

dash.register_page(__name__, path='/pagina5', name='Campo Vectorial',order=5)

layout = html.Div([
    html.Div([
        html.H2("Campo Vectorial 2D (Avanzado)", className="title"),

        html.Div([
            html.Label("Ecuación dx/dt =", style={'fontWeight': 'bold'}),
            dcc.Input(
                id='input-fx',
                type='text',
                value='Y*np.sin(X) - X*np.cos(Y)',
                className="input-field",
                style={'display':'block', 'width':'100%', 'height':'35px', 'padding':'5px', 'font-size':'14px'}
            ),
        ], className="input-group"),

        html.Div([
            html.Label("Ecuación dy/dt =", style={'fontWeight': 'bold'}),
            dcc.Input(
                id='input-fy',
                type='text',
                value='X*np.sin(Y) + Y*np.cos(X)',
                className="input-field",
                style={'display':'block', 'width':'100%', 'height':'35px', 'padding':'5px', 'font-size':'14px'}
            ),
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje X:", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-xmax', type='number', value=5, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Rango del eje Y:", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-ymax', type='number', value=5, className="input-field"),
        ], className="input-group"),

        html.Div([
            html.Label("Mallado:", style={'fontWeight': 'bold'}),
            dcc.Input(id='input-n', type='number', value=15, className="input-field"),
        ], className="input-group"),

        html.Button("Generar gráfica", id='btn-generar', className="btn-generar"),
    ], className="content left"),

    html.Div([
        html.H2("Gráfica del Campo Vectorial", className="title"),

        html.Div([
            dcc.Graph(
                id='grafica-campo',
                style={'height': '430px', 'width': '100%'}
            ),
        ], style={
            'backgroundColor': 'lightblue',
            'padding': '10px',
            'borderRadius': '10px'
        }),

        html.Div(id="info-campo")
    ], className="content right"),

], className="page-container")


@callback(
    [Output("grafica-campo", "figure"),
     Output("info-campo", "children")],
    Input('btn-generar', 'n_clicks'),
    State('input-fx', 'value'),
    State('input-fy', 'value'),
    State('input-xmax', 'value'),
    State('input-ymax', 'value'),
    State('input-n', 'value'),
    prevent_initial_call=False
)
def graficar_campo(n_clicks, fx_str, fy_str, xmax, ymax, n):
    x = np.linspace(-xmax, xmax, n)
    y = np.linspace(-ymax, ymax, n)
    X, Y = np.meshgrid(x, y)
    info_mensaje = ""

    try:
        d = {
            'X': X, 'Y': Y, 'np': np,
            'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
            'exp': np.exp, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e
        }

        fx = eval(fx_str, {}, d)
        fy = eval(fy_str, {}, d)

        magnitud = np.sqrt(fx**2 + fy**2)
        info_mensaje = f"Magnitud Máxima: {magnitud.max():.2f} | Mínima: {magnitud.min():.2f}"

    except Exception as e:
        fx = np.zeros_like(X)
        fy = np.zeros_like(Y)
        info_mensaje = f"Error en las ecuaciones: {e}"

    fig = go.Figure()

    for i in range(n):
        for j in range(n):
            x0, y0 = X[i, j], Y[i, j]
            x1, y1 = x0 + fx[i, j], y0 + fy[i, j]
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines+markers',
                line=dict(color='blue', width=2),
                marker=dict(size=[3, 6], color=["blue", "red"]),
                showlegend=False
            ))

    fig.update_layout(
        title=dict(
            text=f"<b>Campo Vectorial</b>",
            x=0.5, font=dict(size=16, color='green')
        ),
        xaxis_title="X",
        yaxis_title="Y",
        paper_bgcolor='lightblue',
        plot_bgcolor='white',
        font=dict(family='Outfit', size=12, color='black'),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        showline=True, linecolor='black', linewidth=2, mirror=True,
        range=[-xmax*1.1, xmax*1.1]
    )

    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightgray',
        zeroline=True, zerolinewidth=2, zerolinecolor='black',
        showline=True, linecolor='black', linewidth=2, mirror=True,
        range=[-ymax*1.1, ymax*1.1]
    )

    return fig, info_mensaje
