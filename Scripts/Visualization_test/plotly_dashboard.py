import dash
from dash import dcc
from dash import html
import pandas as pd
# import matplotlib as plty
import plotly.express as px
import numpy as np
import plotly.graph_objs as go

# Open dataset
df = pd.read_csv('../../Data/ogd104_stromproduktion_swissgrid.csv', sep=',')

# Open EletricityProductionPlant dataset
df_plants = pd.read_csv('../../Data/ElectricityProductionPlant.csv', sep=',')
df_plants['MainCategory'] = df_plants['MainCategory'].replace(['maincat_1', 'maincat_2', 'maincat_3', 'maincat_4'], [
                                                              'Energie hydraulique', 'Autres énergies renouvelables', 'Energie nucléaire', 'Energie fossile'])

df_1hour = pd.read_csv('../../Data/1hour_concat.csv', sep=',')
# Convertir les dates de type string en type datetime
df_1hour['Date'] = pd.to_datetime(df_1hour['Date'])

df_all_cantons = pd.read_csv('../../Data/all_cantons_installed_production.csv')
df_all_cantons['MainCategory'] = df_all_cantons['MainCategory'].replace(['maincat_1', 'maincat_2', 'maincat_3', 'maincat_4'], [
                                                                        'Energie hydraulique', 'Autres énergies renouvelables', 'Energie nucléaire', 'Energie fossile'])
df_canton_final = {}
for canton in df_plants['Canton'].unique():
    df_canton_final[canton] = df_all_cantons[df_all_cantons['Canton'] == canton]
# Remove all the rows that have a NaN value
df_plants = df_plants.dropna()

# Reindex the dataframe
df_plants = df_plants.reset_index()

# Open cords_WGS84.csv
df_cords_WGS84 = pd.read_csv('../../Data/cords_WGS84.csv', sep=',')

# Store the old column names of both dataframes
cord_column_names = df_cords_WGS84.columns
plants_column_names = df_plants.columns

# Add the coordinates to the original dataframe ignoring the index
df_plants = pd.concat([df_plants, df_cords_WGS84], axis=1, ignore_index=True)

# Rename the columns of the new dataframe
df_plants.columns = plants_column_names.append(cord_column_names)

fig_ch = px.scatter_mapbox(
    df_plants, lat="lat", lon="lon", hover_name="Municipality", zoom=7)
fig_ch.update_layout(mapbox_style="carto-positron",
                     mapbox_center={"lat": 46.8182, "lon": 8.2275},
                     mapbox_zoom=6)

# Create a new dataframe for every different type of energy
df_wind = df[df['Energietraeger'] == 'Wind']
df_thermal = df[df['Energietraeger'] == 'Thermische']
df_storage = df[df['Energietraeger'] == 'Speicherkraft']
df_photovoltaic = df[df['Energietraeger'] == 'Photovoltaik']
df_nuclear = df[df['Energietraeger'] == 'Kernkraft']
df_flow = df[df['Energietraeger'] == 'Flusskraft']

# Translate the german names to english
df_thermal = df_thermal.rename(columns={'Thermische': 'Thermal'})
df_storage = df_storage.rename(columns={'Speicherkraft': 'Storage'})
df_photovoltaic = df_photovoltaic.rename(
    columns={'Photovoltaik': 'Photovoltaic'})
df_nuclear = df_nuclear.rename(columns={'Kernkraft': 'Nuclear'})
df_flow = df_flow.rename(columns={'Flusskraft': 'Flow'})

# Sort the dataframes by date
df_wind = df_wind.sort_values(by=['Datum'])
df_thermal = df_thermal.sort_values(by=['Datum'])
df_storage = df_storage.sort_values(by=['Datum'])
df_photovoltaic = df_photovoltaic.sort_values(by=['Datum'])
df_nuclear = df_nuclear.sort_values(by=['Datum'])
df_flow = df_flow.sort_values(by=['Datum'])

# Create figs for every dataframe
fig_wind = px.line(df_wind, x='Datum', y='Produktion_GWh',
                   title='Wind Production in Switzerland')
fig_wind.update_xaxes(title_text='Date')
fig_wind.update_yaxes(title_text='Production (GWh)')

fig_thermal = px.line(df_thermal, x='Datum', y='Produktion_GWh',
                      title='Thermal Production in Switzerland')
fig_thermal.update_xaxes(title_text='Date')
fig_thermal.update_yaxes(title_text='Production (GWh)')

fig_storage = px.line(df_storage, x='Datum', y='Produktion_GWh',
                      title='Storage Production in Switzerland')
fig_storage.update_xaxes(title_text='Date')
fig_storage.update_yaxes(title_text='Production (GWh)')

fig_photovoltaic = px.line(df_photovoltaic, x='Datum', y='Produktion_GWh',
                           title='Photovoltaic Production in Switzerland')
fig_photovoltaic.update_xaxes(title_text='Date')
fig_photovoltaic.update_yaxes(title_text='Production (GWh)')

fig_nuclear = px.line(df_nuclear, x='Datum', y='Produktion_GWh',
                      title='Nuclear Production in Switzerland')
fig_nuclear.update_xaxes(title_text='Date')
fig_nuclear.update_yaxes(title_text='Production (GWh)')

fig_flow = px.line(df_flow, x='Datum', y='Produktion_GWh',
                   title='Flow Production in Switzerland')
fig_flow.update_xaxes(title_text='Date')
fig_flow.update_yaxes(title_text='Production (GWh)')

df_full = pd.concat([df_wind, df_thermal, df_storage,
                    df_photovoltaic, df_nuclear, df_flow])
fig_full = px.line(df_full, x='Datum', y='Produktion_GWh',
                   color='Energietraeger', title='Energy Production in Switzerland')
fig_full.update_xaxes(title_text='Date')
fig_full.update_yaxes(title_text='Production (GWh)')

# Create the initial figure to display the selected data
fig_selected_data = px.area(df_canton_final["AG"], x='BeginningOfOperation', y='CumulativePower',
                            title='Installed production', color='MainCategory', line_group='MainCategory')

fig_production = px.area(df_1hour, x="Date", y="Production", color='Canton')
fig_consumption = px.area(df_1hour, x="Date", y="Consumption", color='Canton')



# Create a dataframe with

# Initialize the app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Créer le slider pour sélectionner l'année
    dcc.DatePickerRange(
        id='date-picker-range',
        min_date_allowed=df_1hour['Date'].min(),
        max_date_allowed=df_1hour['Date'].max(),
        start_date=df_1hour['Date'].min(),
        end_date=df_1hour['Date'].max()
    ),
    dcc.Dropdown(
        id="filter-canton_graph",
        options=[{'label': c, 'value': c} for c in df_1hour['Canton'].unique(
        )] + [{'label': 'ALL', 'value': 'all'}],
        multi=False,
        value="AG",
        style={'width': '50%'}
    ),
    # Display the figures side by side
    html.Div([
        # Display the map
        dcc.Graph(id='graph_ch', figure=fig_ch)
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        # Display the selected data
        dcc.Graph(id='graph_selected_data', figure=fig_selected_data)
    ], style={'width': '50%', 'display': 'inline-block'}),

    # # # Display the wind dataframe
    # dcc.Graph(id='graph_wind', figure=fig_wind,style={'display': 'block'}),

    # # Display the thermal dataframe
    # dcc.Graph(id='graph_thermal', figure=fig_thermal),

    # # Display the storage dataframe
    # dcc.Graph(id='graph_storage', figure=fig_storage),

    # # Display the photovoltaic dataframe
    # dcc.Graph(id='graph_photovoltaic', figure=fig_photovoltaic),

    # # Display the nuclear dataframe
    # dcc.Graph(id='graph_nuclear', figure=fig_nuclear),

    # # Display the flow dataframe
    # dcc.Graph(id='graph_flow', figure=fig_flow),

    # # Display the full dataframe
    # dcc.Graph(id='graph_full', figure = fig_full),

    html.Div([
        # graphique 1
        dcc.Graph(
            id='graph1',
            figure=fig_production,
            style={'display': 'block'}
        ),
        # graphique 2
        dcc.Graph(
            id='graph2',
            figure=fig_consumption,
            style={'display': 'none'}
        ),
        # bouton pour switcher les graphiques
        html.Button('Switch', id='switch-button')
    ])
])

# Switch entre les graph prod et conso
@app.callback(
    [dash.dependencies.Output('graph1', 'style'),
     dash.dependencies.Output('graph2', 'style')],
    [dash.dependencies.Input('switch-button', 'n_clicks')]
)
def switch_graphs(n_clicks):
    if n_clicks is None:
        return {'display': 'block'}, {'display': 'none'}
    if n_clicks % 2 == 1:
        return {'display': 'block'}, {'display': 'none'}
    else:
        return {'display': 'none'}, {'display': 'block'}



# Mettre à jour les figures
@app.callback(
    [dash.dependencies.Output('graph_ch', 'figure'), dash.dependencies.Output(
        'graph_selected_data', 'figure'), dash.dependencies.Output('graph1', 'figure'),
     dash.dependencies.Output('graph2', 'figure')],
    [dash.dependencies.Input('filter-canton_graph', 'value'), dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')]
)
def update_figures(selected_cantons, start_date, end_date):
    # Filter the data by the selected cantons
    if selected_cantons == "all" or selected_cantons == None:

        # Map + Installed power
        map = fig_ch
        fig_installed_power = px.area(df_all_cantons, x='BeginningOfOperation', y='CumulativePower',
                                      title='Total Installed production', color='MainCategory', line_group='MainCategory')

        # Prod + Cons
        filtered_data = df_1hour  # Update the figure to display the selected data
        fig_production = px.area(
            df_1hour, x="Date", y="Production", color='Canton')
        fig_consumption = px.area(
            df_1hour, x="Date", y="Consumption", color='Canton')

    elif (selected_cantons not in df_plants["Canton"].unique() and selected_cantons in df_1hour['Canton'].unique()):
        map = fig_ch
        fig_installed_power = px.area(df_all_cantons, x='BeginningOfOperation', y='CumulativePower',
                                      title='Total Installed production', color='MainCategory', line_group='MainCategory')
        filtered_data = df_1hour[(df_1hour['Canton'] == selected_cantons) &
                                 (df_1hour['Date'] >= start_date) &
                                 (df_1hour['Date'] <= end_date)]
        fig_production = px.area(
            filtered_data, x="Date", y="Production", title="Production " + selected_cantons)
        fig_consumption = px.area(
            filtered_data, x="Date", y="Consumption", title="Consumption " + selected_cantons)
    else:
        # Map + Intalled power
        filtered_data_map = df_plants.loc[df_plants['Canton']
                                          == selected_cantons]
        # Update the figure to display the selected data
        fig_installed_power = px.area(df_canton_final[selected_cantons], x='BeginningOfOperation', y='CumulativePower',
                                      title='Installed production ' + selected_cantons, color='MainCategory', line_group='MainCategory')
        # Prod + cons
        filtered_data = df_1hour[(df_1hour['Canton'] == selected_cantons) &
                                 (df_1hour['Date'] >= start_date) &
                                 (df_1hour['Date'] <= end_date)]

        map = px.scatter_mapbox(
            filtered_data_map, lat="lat", lon="lon", hover_name="Municipality", zoom=7, color="MainCategory")
        map.update_layout(mapbox_style="carto-positron",
                          mapbox_center={
                              "lat": 46.8182, "lon": 8.2275},
                          mapbox_zoom=6)

        fig_production = px.area(
            filtered_data, x="Date", y="Production", title="Production " + selected_cantons)
        fig_consumption = px.area(
            filtered_data, x="Date", y="Consumption", title="Consumption " + selected_cantons)

    # Return the updated figures
    return fig_installed_power, map, fig_production, fig_consumption


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
