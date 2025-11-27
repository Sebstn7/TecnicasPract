import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import plotly.graph_objs as go
from scipy.integrate import odeint

# Registra la página (si usas multipage) o app = dash.Dash(__name__) si es standalone
dash.register_page(__name__, path='/pagina10', name='Gilpin-Ayala Impulsivo')

layout = html.Div([
    html.Div([
        html.H2("Modelo Gilpin-Ayala con Cosecha Impulsiva (2.2)", className="title"),

        # --- PARÁMETROS BIOLÓGICOS (IGUAL QUE ANTES) ---
        html.H4("Parámetros Biológicos"),
        html.Div([
            html.Div([
                html.Label("Tasa crec. presa (r):"), 
                dcc.Input(id='i-r', type='number', value=0.25, step=0.01, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Capacidad carga (K):"), 
                dcc.Input(id='i-K', type='number', value=10, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Exponente (α):"), 
                dcc.Input(id='i-alpha', type='number', value=0.5, step=0.01, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Captura (τ1):"), 
                dcc.Input(id='i-tau1', type='number', value=0.33, step=0.01, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Conversión (τ2):"), 
                dcc.Input(id='i-tau2', type='number', value=0.2, step=0.01, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Semi-saturación (β):"), 
                dcc.Input(id='i-beta', type='number', value=3.5, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Mortalidad (ω):"), 
                dcc.Input(id='i-omega', type='number', value=0.1, step=0.01, className="input-field")
                ], className="input-group"),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}),

        html.Hr(),

        # --- NUEVOS PARÁMETROS DE CONTROL IMPULSIVO ---
        html.H4("Estrategia de Cosecha"),
        html.Div([
            html.Div([
                html.Label("Peso Presa (μ):"), 
                dcc.Input(id='i-mu', type='number', value=0.5, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Umbral de Cosecha (I):"), 
                dcc.Input(id='i-I', type='number', value=1.5, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Intensidad (h):"),
                dcc.Input(id='i-h', type='number', value=0.8, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Tasa captura Presa (c1):"), 
                dcc.Input(id='i-c1', type='number', value=0.7, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Tasa captura Dep. (c2):"), 
                dcc.Input(id='i-c2', type='number', value=0.3, step=0.1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Liberación Dep. (Λ):"), 
                dcc.Input(id='i-Lambda', type='number', value=0.0, step=0.1, className="input-field")
                ], className="input-group"),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}),

        html.Hr(),

        # --- CONDICIONES INICIALES ---
        html.H4("Valores Iniciales"),
        html.Div([
            html.Div([
                html.Label("A0:"), 
                dcc.Input(id='i-A0', type='number', value=4, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("B0:"), 
                dcc.Input(id='i-B0', type='number', value=1, className="input-field")
                ], className="input-group"),
            html.Div([
                html.Label("Tiempo Máx:"), 
                dcc.Input(id='i-tiempo', type='number', value=200, className="input-field")
                ], className="input-group"),
        ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}),

        html.Button("Simular Sistema Impulsivo", id='btn-simular-imp', className="btn-generar", style={'marginTop': '20px'}),

    ], className="content left"),

    html.Div([
        html.H2("Dinámica con Pulsos", className="title"),
        dcc.Graph(
            id='grafica-impulsiva-tiempo',
            style={'height': '450px', 'width': '100%'}),
        dcc.Graph(
            id='grafica-impulsiva-fase',
            style={'height': '450px', 'width': '100%'}),
    ], className="content right"),

], className="page-container")

# --- ECUACIONES DIFERENCIALES (PARTE CONTINUA) ---
def sistema_continuo(y, t, r, K, alpha, tau1, tau2, beta, omega):
    A, B = y
    # Evitar valores negativos o cero que rompan la potencia fraccionaria alpha
    if A < 0: A = 0
    if B < 0: B = 0
    
    dA_dt = r * A * (1 - (A/K)**alpha) - (tau1 * A**2 * B) / (A**2 + beta)
    dB_dt = (tau2 * A**2 / (A**2 + beta) - omega) * B
    return [dA_dt, dB_dt]

# --- CALLBACK ---
@callback(
    [Output('grafica-impulsiva-tiempo', 'figure'),
     Output('grafica-impulsiva-fase', 'figure')],
    Input('btn-simular-imp', 'n_clicks'),
    [State('i-r', 'value'), 
     State('i-K', 'value'), 
     State('i-alpha', 'value'),
     State('i-tau1', 'value'), 
     State('i-tau2', 'value'), 
     State('i-beta', 'value'), 
     State('i-omega', 'value'),
     State('i-mu', 'value'), 
     State('i-I', 'value'), 
     State('i-h', 'value'),
     State('i-c1', 'value'), 
     State('i-c2', 'value'), 
     State('i-Lambda', 'value'),
     State('i-A0', 'value'), 
     State('i-B0', 'value'), 
     State('i-tiempo', 'value')]
)
def simular_sistema_hibrido(n_clicks, r, K, alpha, tau1, tau2, beta, omega, mu, I, h, c1, c2, Lambda, A0, B0, t_max):
    
    # Configuración del paso de tiempo
    dt = 0.1  # Paso pequeño para detectar el evento
    t_current = 0
    A_current, B_current = A0, B0
    
    # Listas para guardar la historia (incluyendo los saltos)
    t_history = [0]
    A_history = [A0]
    B_history = [B0]
    
    # Listas auxiliares para dibujar las líneas de "pesca" (los saltos verticales)
    saltos_x = []
    saltos_y = []

    # --- BUCLE DE SIMULACIÓN HÍBRIDA ---
    while t_current < t_max:
        # 1. Verificar condición de impulso (Conjunto M)
        # Ecuación: mu*A + (1-mu)*B = I
        valor_control = mu * A_current + (1 - mu) * B_current
        
        if valor_control >= I:
            # --- APLICAR IMPULSO (Salto) ---
            A_new = (1 - c1 * h) * A_current
            B_new = (1 - c2 * h) * B_current + Lambda
            
            # Guardar el punto exacto antes del salto (para la gráfica)
            t_history.append(t_current)
            A_history.append(A_current)
            B_history.append(B_current)
            
            # Guardar el punto exacto después del salto (crea la línea vertical)
            t_history.append(t_current)
            A_history.append(A_new)
            B_history.append(B_new)
            
            # Actualizar estado actual
            A_current = A_new
            B_current = B_new
            
            # Evitar bucles infinitos si el salto cae justo en el umbral de nuevo
            # Avanzamos un micro paso artificialmente
            t_current += 0.001 
            
        else:
            # --- DINÁMICA CONTINUA ---
            t_next = t_current + dt
            # Integramos solo un paso de tiempo
            sol = odeint(sistema_continuo, [A_current, B_current], [t_current, t_next], 
                         args=(r, K, alpha, tau1, tau2, beta, omega))
            
            A_next, B_next = sol[-1]
            
            # Actualizar listas
            t_history.append(t_next)
            A_history.append(A_next)
            B_history.append(B_next)
            
            # Actualizar estado
            A_current = A_next
            B_current = B_next
            t_current = t_next

    # --- GRÁFICA 1: SERIES DE TIEMPO ---
    fig_tiempo = go.Figure()
    fig_tiempo.add_trace(go.Scatter(
        x=t_history, 
        y=A_history, 
        name='Presas (A)', 
        line=dict(color='blue'),
        hovertemplate='tiempo %{x:.0f}<br>Presas: %{y:.2f}<extra></extra>'
        )
    )
    fig_tiempo.add_trace(go.Scatter(
        x=t_history, 
        y=B_history, 
        name='Depredadores (B)', 
        line=dict(color='red'),
        hovertemplate='tiempo %{x:.0f}<br>Depredadores: %{y:.2f}<extra></extra>'
        )
    )
    
    # Línea del umbral (aproximada, solo conceptual si B fuera constante, difícil de dibujar fija en t)
    # Pero podemos añadir una línea horizontal de referencia si mu=1 (solo depende de A)
    
    fig_tiempo.update_layout(
        title=dict(
            text = "<b>Evolución Temporal con Impulsos</b>",
            x = 0.5, 
            font=dict(size=16, color='darkblue') 
        ),
        xaxis_title="Tiempo", 
        yaxis_title="Población",
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

    fig_tiempo.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    fig_tiempo.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    # --- GRÁFICA 2: PLANO DE FASE ---
    fig_fase = go.Figure()
    
    # Trayectoria
    fig_fase.add_trace(go.Scatter(
        x=A_history, 
        y=B_history, 
        mode='lines', 
        name='Trayectoria', 
        line=dict(color='green'),
        hovertemplate='Presas %{x:.2f}<br>Depredadores: %{y:.2f}<extra></extra>'
        )
    )
    
    # Dibujar la Línea de Impulso (M) y la Línea de Fase (N)
    # M: mu*A + (1-mu)*B = I  =>  B = (I - mu*A) / (1-mu)
    # N: Ecuación derivada anteriormente
    
    A_range = np.linspace(0, K, 100)
    if mu != 1:
        B_M = (I - mu * A_range) / (1 - mu)
        # Ecuación de N simplificada para graficar
        # mu*A/(1-c1*h) + (1-mu)*B/(1-c2*h) = I + (1-mu)*Lambda/(1-c2*h)
        C_const = I + ((1-mu)*Lambda)/(1 - c2*h)
        B_N = (C_const - (mu * A_range)/(1 - c1*h)) * ((1 - c2*h)/(1 - mu))
        
        fig_fase.add_trace(go.Scatter(
            x=A_range, 
            y=B_M, 
            name='C. Pulso (M)', 
            line=dict(dash='dash', color='orange'),
            hovertemplate='Presas %{x:.2f}<br>Depredadores: %{y:.2f}<extra></extra>'
            )
        )
        fig_fase.add_trace(go.Scatter(
            x=A_range, 
            y=B_N, 
            name='C. Fase (N)', 
            line=dict(dash='dot', color='purple'),
            hovertemplate='Presas %{x:.2f}<br>Depredadores: %{y:.2f}<extra></extra>'
            )
        )
    else:
        # Si mu=1, las líneas son verticales A = I y A = I(1-c1h)
        fig_fase.add_vline(x=I, line_dash="dash", line_color="orange", annotation_text="M")
        fig_fase.add_vline(x=I*(1-c1*h), line_dash="dot", line_color="purple", annotation_text="N")

    fig_fase.update_layout(
        title=dict(
            text = "<b>Plano de Fase (A vs B)</b>",
            x = 0.5, 
            font=dict(size=16, color='darkblue') 
        ),
        xaxis_title="Presas (A)", 
        yaxis_title="Depredadores (B)",
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
        xaxis=dict(range=[0, K+1]),
        yaxis=dict(range=[0, max(B_history)*1.1]),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    fig_fase.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    fig_fase.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='lightpink', 
        zeroline=True, zerolinewidth= 2,zerolinecolor='black',
    )

    return fig_tiempo, fig_fase