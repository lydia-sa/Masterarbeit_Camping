# IMPORT LIBRARIES
#-------------------------------------------------------------------
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq

# BILDER IMPORTIEREN
#-------------------------------------------------------------------
image_path = '../assets/doppelt.png'
image_path_ = '../assets/vorbereitung.png'

# START APP
#-------------------------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

# LAYOUT
#--------------------------------------------------------------------

# Layout der App definieren
app.layout = html.Div([
    dbc.Container([
    # Titelzeile
    html.H3(' *** ', style={'text-align': 'center', 'font-family': 'Arial', 'font-size': '50px', 'font-weight': 'bold', 'color': '#FFFFFF'}),
    html.H3('Campingpreise in der Schweiz', style={'text-align': 'center', 'font-family': 'Arial', 'font-size': '34px', 'font-weight': 'bold', 'color': '#26707C'}),
    html.H3('Analyse von Angeboten und Einflussfaktoren', style={'text-align': 'center', 'font-family': 'Arial', 'font-size': '20px', 'font-weight': 'bold', 'color': '#26707C'}),


]),
    dbc.Row([
        dbc.Col([html.H5('These 3'),
                 html.P('Die Stellplatzgrösse und die Saisonalität sind die entscheidenden Faktoren für die Preisgestaltung der Campingplätze in der Schweiz.'),
                 html.H3(' *** ', style={'text-align': 'center', 'font-family': 'Arial', 'font-size': '10px', 'font-weight': 'bold', 'color': '#FFFFFF'}),

                 # Toggle-Schalter hinzufügen
                 daq.BooleanSwitch(
                     id='toggle-fazit',
                     on= False,
                     color='#26707C',
                     style={'margin-bottom': '20px'}
                 ),

                 html.Div(id='fazit-container', children=[
                 html.H5('Fazit'),
                 html.P('Grössere Stellplätze und Hauptsaisonzeit sind entscheidende Faktoren für die Preisgestaltung. Sie führen tendenziell zu höheren Preisen.'),
                 ], style={'display': 'none'})  # Anfangs nicht sichtbar
                 ], style={'width':{'size': 2}, 'float': 'left', 'padding': '50px'}),

        dbc.Col([
            dcc.Dropdown(id='dataset-dropdown',
                         options=[
                             {'label': 'Datzensatz doppelt', 'value': 'doppelt'},
                             {'label': 'Datensatz vorbereitet', 'value': 'vorbereitet'}],

                         value='doppelt',
                         style={'width': '95%'}
                         ),
            html.Img(id='image', src=app.get_asset_url('doppelt.png'), style={'width': '92%'})
        ], width={'size': 9}),

])

])



# Callback für das Aktualisieren der Grafiken basierend auf der Auswahl im Dropdown
@app.callback(
    Output('image', 'src'),
    Input('dataset-dropdown', 'value'))

def update_image(selected_dataset):
    if selected_dataset == 'doppelt':
        return app.get_asset_url('doppelt.png')
    else:
        return app.get_asset_url('vorbereitung.png')

# Callback für das Anzeigen/Verbergen des Fazit-Bereichs
@app.callback(
    Output('fazit-container', 'style'),
    Input('toggle-fazit', 'on')
)
def toggle_fazit_display(toggle_value):
    if toggle_value:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# App ausführen
if __name__ == '__main__':
    app.run_server(debug=True)
