import dash
from dash import html, dcc

dash.register_page(__name__, path='/', name='Inicio', order =1)

layout = html.Div([
    html.Div([
        html.H1("Sebastián Porras", style={
            'textAlign': 'center', 
            'color': '#1e3a5f',
            'marginBottom': '10px',
            'fontFamily': 'Arial, sans-serif',
            'fontSize': '2.5em'
        }),
        html.Hr(style={'width': '80px', 'margin': '20px auto', 'border': '2px solid #2c5aa0'}),
        html.P("Estudiante de Computación Científica", style={
            'textAlign': 'center',
            'color': '#5d6d7e',
            'fontSize': '20px',
            'marginBottom': '40px',
            'fontWeight': '300'
        })
    ], style={'padding': '60px 20px', 'backgroundColor': '#f8f6f0'}),
    
    html.Div([
        html.Div([
            html.H2([
                html.I(className="fas fa-tools", style={'marginRight': '10px', 'color': '#1e3a5f'}),
                "Habilidades Técnicas"
            ], style={
                'color': '#1e3a5f', 
                'borderBottom': '2px solid #2c5aa0',
                'paddingBottom': '10px',
                'display': 'flex',
                'alignItems': 'center'
            }),
            
            html.Div([
                html.H3([
                    html.I(className="fas fa-code", style={'marginRight': '10px', 'color': '#2c5aa0'}),
                    "Lenguajes de Programación"
                ], style={'color': '#2c3e50', 'marginTop': '25px', 'display': 'flex', 'alignItems': 'center'}),
                html.Ul([
                    html.Li([html.I(className="fab fa-python", style={'marginRight': '8px', 'color': '#2c5aa0'}), "Python"]),
                    html.Li([html.I(className="fas fa-cube", style={'marginRight': '8px', 'color': '#1e3a5f'}), "C++ con OpenGL"]),
                    html.Li([html.I(className="fas fa-database", style={'marginRight': '8px', 'color': '#2c5aa0'}), "SQL"]),
                    html.Li([html.I(className="fab fa-js-square", style={'marginRight': '8px', 'color': '#2c5aa0'}), "JavaScript"]),
                ], style={'color': '#34495e', 'lineHeight': '2.0', 'fontSize': '16px', 'listStyle': 'none', 'padding': '0'}),
                
                html.H3([
                    html.I(className="fas fa-globe", style={'marginRight': '10px', 'color': '#2c5aa0'}),
                    "Desarrollo Web"
                ], style={'color': '#2c3e50', 'marginTop': '25px', 'display': 'flex', 'alignItems': 'center'}),
                html.Ul([
                    html.Li([html.I(className="fab fa-html5", style={'marginRight': '8px', 'color': '#1e3a5f'}), "HTML5"]),
                    html.Li([html.I(className="fab fa-css3-alt", style={'marginRight': '8px', 'color': '#2c5aa0'}), "CSS3"]),
                    html.Li([html.I(className="fas fa-chart-line", style={'marginRight': '8px', 'color': '#2c5aa0'}), "Dash Framework"]),
                ], style={'color': '#34495e', 'lineHeight': '2.0', 'fontSize': '16px', 'listStyle': 'none', 'padding': '0'})
            ])
        ], style={'flex': '1', 'padding': '40px', 'backgroundColor': '#ffffff', 'borderRadius': '8px', 'boxShadow': '0 4px 12px rgba(30,58,95,0.1)'}),
        
        html.Div([
            html.H2([
                html.I(className="fas fa-envelope", style={'marginRight': '10px', 'color': '#2c5aa0'}),
                "Contacto"
            ], style={
                'color': '#1e3a5f',
                'borderBottom': '2px solid #2c5aa0',
                'paddingBottom': '10px',
                'display': 'flex',
                'alignItems': 'center'
            }),
            
            html.Div([
                html.Div([
                    html.I(className="fas fa-envelope", style={'marginRight': '10px', 'color': '#1e3a5f'}),
                    html.Span("s3bastianporras@gmail.com")
                ], style={'margin': '20px 0', 'fontSize': '16px', 'color': '#2c3e50', 'display': 'flex', 'alignItems': 'center'})
            ]),
            
            html.H3([
                html.I(className="fas fa-link", style={'marginRight': '10px', 'color': '#2c5aa0'}),
                "Enlaces"
            ], style={'color': '#1e3a5f', 'marginTop': '30px', 'marginBottom': '20px', 'display': 'flex', 'alignItems': 'center'}),
            
            html.Div([
                html.A(
                    [
                        html.I(className="fab fa-github", style={'marginRight': '10px'}),
                        html.Span("GitHub")
                    ], 
                    href="https://github.com/Sebstn7", 
                    target="_blank",
                    style={
                        'display': 'flex', 
                        'alignItems': 'center',
                        'justifyContent': 'center',
                        'padding': '12px 20px', 
                        'margin': '10px 0', 
                        'backgroundColor': '#1e3a5f', 
                        'color': 'white', 
                        'textDecoration': 'none', 
                        'borderRadius': '5px',
                        'fontWeight': '500'
                    }
                )
            ])
        ], style={'flex': '1', 'padding': '40px', 'backgroundColor': '#f0f4f8', 'borderRadius': '8px', 'marginLeft': '20px'})
    ], style={
        'display': 'flex', 
        'maxWidth': '1200px', 
        'margin': '0 auto', 
        'padding': '40px 20px',
        'gap': '30px'
    })
], style={
    'fontFamily': 'Arial, sans-serif', 
    'minHeight': '100vh',
    'backgroundColor': '#ffffff'
})