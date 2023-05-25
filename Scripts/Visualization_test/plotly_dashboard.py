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
df_plants = pd.read_csv('../../Data/ProductionPlantFix.csv', sep=',')
df_plants['MainCategory'] = df_plants['MainCategory'].replace(['maincat_1', 'maincat_2', 'maincat_3', 'maincat_4'], [
                                                              'Energie hydraulique', 'Autres énergies renouvelables', 'Energie nucléaire', 'Energie fossile'])

# Create a color dictionary for the different types of energy
color_dict = {'Energie hydraulique': 'rgb(0, 0, 255)', 'Autres énergies renouvelables': 'rgb(0, 255, 0)',
              'Energie nucléaire': 'rgb(255, 0, 0)', 'Energie fossile': 'rgb(0, 0, 0)'}

df_1hour = pd.read_csv('../../Data/1hour_concat.csv', sep=',')
# Convertir les dates de type string en type datetime
df_1hour['Date'] = pd.to_datetime(df_1hour['Date'])

df_pc = df_1hour
df_pc = df_pc.sort_values(by=['Date', 'Canton'])
df_pc = df_pc.reset_index(drop=True)
# Multiply consumption by -1 to get a negative value
df_pc['Consumption'] = df_pc['Consumption'] * -1

# Remove the rows with a production or consumption value of 0
df_pc = df_pc[df_pc.Production != 0]
df_pc = df_pc[df_pc.Consumption != 0]
# reindex the dataframe
df_pc = df_pc.reset_index(drop=True)
# Calculer les totaux de production et de consommation par date
totals = df_pc.groupby('Date').agg(
    {'Production': 'sum', 'Consumption': 'sum'}).reset_index()
totals['Canton'] = 'CH'
totals = totals[['Date', 'Production', 'Consumption', 'Canton']]

df_pc = pd.concat([df_pc, totals], ignore_index=True)
df_pc['ProdConsSum'] = df_pc['Production'] + df_pc['Consumption']

df_installed_cantons = pd.read_csv(
    '../../Data/all_cantons_installed_production_with_CH.csv', sep=',')
df_installed_CH = df_installed_cantons[df_installed_cantons['Canton'] == 'CH']
df_all_cantons = pd.read_csv('../../Data/all_cantons_installed_production.csv')
df_all_cantons['MainCategory'] = df_all_cantons['MainCategory'].replace(['maincat_1', 'maincat_2', 'maincat_3', 'maincat_4'], [
                                                                        'Energie hydraulique', 'Autres énergies renouvelables', 'Energie nucléaire', 'Energie fossile'])
df_installed_CH['MainCategory'] = df_installed_CH['MainCategory'].replace(['maincat_1', 'maincat_2', 'maincat_3', 'maincat_4'], [
    'Energie hydraulique', 'Autres énergies renouvelables', 'Energie nucléaire', 'Energie fossile'])
df_canton_final = {}
for canton in df_plants['Canton'].unique():
    df_canton_final[canton] = df_all_cantons[df_all_cantons['Canton'] == canton]

# Open cords_WGS84.csv
df_cords_WGS84 = pd.read_csv('../../Data/cords_WGS84.csv', sep=',')

# Store the old column names of both dataframes
cord_column_names = df_cords_WGS84.columns
plants_column_names = df_plants.columns

# Add the coordinates to the original dataframe ignoring the index
# df_plants = pd.concat([df_plants, df_cords_WGS84], axis=1, ignore_index=True)

# Rename the columns of the new dataframe
# df_plants.columns = plants_column_names.append(cord_column_names)

fig_ch = px.scatter_mapbox(
    df_plants, lat="lat", lon="lon", hover_name="Municipality", hover_data="TotalPower", zoom=7, color='MainCategory', color_discrete_map=color_dict)
fig_ch.update_layout(mapbox_style="carto-positron",
                     mapbox_center={"lat": 46.8182, "lon": 8.2275},
                     mapbox_zoom=6,
                     )

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
fig_wind.update_yaxes(title_text='Production [GWh/Day]')

fig_thermal = px.line(df_thermal, x='Datum', y='Produktion_GWh',
                      title='Thermal Production in Switzerland')
fig_thermal.update_xaxes(title_text='Date')
fig_thermal.update_yaxes(title_text='Production [GWh/Day]')

fig_storage = px.line(df_storage, x='Datum', y='Produktion_GWh',
                      title='Storage Production in Switzerland')
fig_storage.update_xaxes(title_text='Date')
fig_storage.update_yaxes(title_text='Production [GWh/Day]')

fig_photovoltaic = px.line(df_photovoltaic, x='Datum', y='Produktion_GWh',
                           title='Photovoltaic Production in Switzerland')
fig_photovoltaic.update_xaxes(title_text='Date')
fig_photovoltaic.update_yaxes(title_text='Production [GWh/Day]')

fig_nuclear = px.line(df_nuclear, x='Datum', y='Produktion_GWh',
                      title='Nuclear Production in Switzerland')
fig_nuclear.update_xaxes(title_text='Date')
fig_nuclear.update_yaxes(title_text='Production [GWh/Day]')

# Créez une liste d'options pour le menu déroulant
graph_options = [
    {'label': 'Wind', 'value': 'graph_wind'},
    {'label': 'Thermal', 'value': 'graph_thermal'},
    {'label': 'Storage', 'value': 'graph_storage'},
    {'label': 'Photovoltaic', 'value': 'graph_photovoltaic'},
    {'label': 'Nuclear', 'value': 'graph_nuclear'},
    {'label': 'Flow', 'value': 'graph_flow'},
    {'label': 'Full', 'value': 'graph_full'}
]

fig_flow = px.line(df_flow, x='Datum', y='Produktion_GWh',
                   title='Flow Production in Switzerland')
fig_flow.update_xaxes(title_text='Date')
fig_flow.update_yaxes(title_text='Production [GWh/Day]')

df_full = pd.concat([df_wind, df_thermal, df_storage,
                    df_photovoltaic, df_nuclear, df_flow])
fig_full = px.line(df_full, x='Datum', y='Produktion_GWh',
                   color='Energietraeger', title='Energy Production in Switzerland')
fig_full.update_xaxes(title_text='Date')
fig_full.update_yaxes(title_text='Production [GWh/Day]')

# Create the initial figure to display the selected data
fig_selected_data = px.area(df_canton_final["AG"], x='BeginningOfOperation', y='CumulativePower',
                            title='Installed production', color='MainCategory', line_group='MainCategory', color_discrete_map=color_dict)

fig_production = px.area(df_1hour, x="Date", y="Production", color='Canton')
fig_consumption = px.area(df_1hour, x="Date", y="Consumption", color='Canton')

fig_prod_cons = px.line(df_pc, x='Date', y=[
                        'Production', 'Consumption'], title='Production and Consumption')


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
        options=[{'label': c, 'value': c} for c in df_plants['Canton'].unique(
        )] + [{'label': 'ALL', 'value': 'all'}],

        multi=False,
        value="AG",
        style={'width': '50%'}
    ),
    html.Div([
        dcc.RangeSlider(
            df_plants["TotalPower"].min(), df_plants["TotalPower"].max(), 40000, value=[df_plants["TotalPower"].min(), df_plants["TotalPower"].max()],
            id='power-slider'
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),
    # Display the figures side by side
    html.Div([
        # Display the map
        dcc.Graph(id='graph_ch', figure=fig_ch)
    ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        # Display the selected data
        dcc.Graph(id='graph_selected_data', figure=fig_selected_data)
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='graph_prod_cons', figure=fig_prod_cons),
        html.Button('Toggle Prod-Cons Trace', id='toggle-button', n_clicks=0)
    ], style={'margin-bottom' : '50px'}),
    html.Div([
        # Ajoutez le menu déroulant
        dcc.Dropdown(
            id='graph-dropdown',
            options=graph_options,
            value='graph_wind'
        ),
        # Ajoutez le conteneur pour afficher les graphiques
        html.Div(id='graph-container')
    ])

])

@app.callback(
    [dash.dependencies.Output('graph_ch', 'figure'), dash.dependencies.Output(
        'graph_selected_data', 'figure'), dash.dependencies.Output(
        'graph_prod_cons', 'figure')],
    [dash.dependencies.Input('filter-canton_graph', 'value'), dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date'), dash.dependencies.Input('toggle-button', 'n_clicks'), dash.dependencies.Input('power-slider', 'value')]
)
def update_figures(selected_cantons, start_date, end_date, n_clicks, power_range):
    min_power, max_power = power_range
    filter_all = df_pc[(df_pc['Canton'] == 'CH') &
                       (df_pc['Date'] >= start_date) &
                       (df_pc['Date'] <= end_date)]
    filter_canton = df_pc[(df_pc['Canton'] == selected_cantons) &
                          (df_pc['Date'] >= start_date) &
                          (df_pc['Date'] <= end_date)]
    group_canton_name = ""
    # Filter the data by the selected cantons
    if selected_cantons == "all" or selected_cantons == None:

        # Map + Installed power
        filtered_data_map = df_plants[(df_plants['TotalPower'] >= min_power) &
                                      (df_plants['TotalPower'] <= max_power)]

        fig_installed_power = px.area(df_installed_CH, x='BeginningOfOperation', y='CumulativePower',
                                      title='Total Installed production', color='MainCategory', line_group='MainCategory', color_discrete_map=color_dict)
        fig_installed_power.update_layout(yaxis=dict(title='kW'))
        # Prod + Cons
        filtered_data = filter_all
        fig_prod_cons = px.line(filtered_data, x='Date', y=[
                                'Production', 'Consumption'], title='Total Production and Consumption')
        fig_prod_cons.update_layout(yaxis=dict(title='kWh'))

    else:
        # Map + Intalled power
        filtered_data_map = df_plants[(df_plants['Canton'] == selected_cantons) &
                                      (df_plants['TotalPower'] >= min_power) &
                                      (df_plants['TotalPower'] <= max_power)]
        # Update the figure to display the selected data
        fig_installed_power = px.area(df_canton_final[selected_cantons], x='BeginningOfOperation', y='CumulativePower',
                                      title='Installed production ' + selected_cantons, color='MainCategory', line_group='MainCategory', color_discrete_map=color_dict)
        fig_installed_power.update_layout(yaxis=dict(title='kW'))

        if selected_cantons == "GE" or selected_cantons == "VD":
            group_canton_name = "GE/VD"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption ' + group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "BL" or selected_cantons == "BS":
            group_canton_name = "BL/BS"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption ' + group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "AI" or selected_cantons == "AR":
            group_canton_name = "AI/AR"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption ' + group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "SH" or selected_cantons == "ZH":
            group_canton_name = "SH/ZH"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption ' + group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "SZ" or selected_cantons == "ZG":
            group_canton_name = "SZ/ZG"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption '+group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "BE" or selected_cantons == "JU":
            group_canton_name = "BE/JU"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption '+group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        elif selected_cantons == "OW" or selected_cantons == "NW" or selected_cantons == "UR":
            group_canton_name = "OW/NW/UR"
            filter_canton = df_pc[(df_pc['Canton'] == group_canton_name) &
                                  (df_pc['Date'] >= start_date) &
                                  (df_pc['Date'] <= end_date)]
            fig_prod_cons = px.line(filter_canton, x='Date', y=[
                                    'Production', 'Consumption'], title='Production and Consumption '+group_canton_name)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        else:
            group_canton_name = selected_cantons
            filtered_data = filter_canton
            fig_prod_cons = px.line(filtered_data, x='Date', y=[
                'Production', 'Consumption'], title='Production and Consumption ' + selected_cantons)
            fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
    # Vérifier si le bouton "Toggle Prod-Cons Trace" a été cliqué
    if n_clicks % 2 == 1 and selected_cantons != "all":
        # Filtrer les données en fonction du canton et de la date sélectionnés
        filtered_data = filter_canton

        # Créer la figure avec la ligne de somme
        fig_prod_cons = px.line(filtered_data, x='Date', y=[
                                'Production', 'Consumption', 'ProdConsSum'], title='Production and Consumption ' + group_canton_name)
        fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
        fig_prod_cons.update_traces(
            line=dict(dash='dash', width=2.5), selector=dict(name='ProdConsSum'))
    elif n_clicks % 2 == 1 and selected_cantons == "all":
        filtered_data = filter_all
        fig_prod_cons = px.line(filtered_data, x='Date', y=[
                                'Production', 'Consumption', 'ProdConsSum'], title='Production and Consumption Total')
        fig_prod_cons.update_layout(yaxis=dict(title='kWh'))
    else:
        fig_prod_cons = fig_prod_cons
    map = px.scatter_mapbox(
        filtered_data_map, lat="lat", lon="lon", hover_name="Municipality", hover_data="TotalPower", zoom=7, color="MainCategory", color_discrete_map=color_dict)
    map.update_layout(mapbox_style="carto-positron",
                      mapbox_center={
                          "lat": 46.8182, "lon": 8.2275},
                      mapbox_zoom=6)

    # Return the updated figures
    return fig_installed_power, map, fig_prod_cons


@app.callback(
    dash.dependencies.Output('graph-container', 'children'),
    dash.dependencies.Input('graph-dropdown', 'value')
)
def update_droptown_graph(selected_graph):
    # Sélectionnez le graphique correspondant à la valeur sélectionnée dans le menu déroulant
    if selected_graph == 'graph_wind':
        return dcc.Graph(id='graph_wind', figure=fig_wind, style={'display': 'block'})
    elif selected_graph == 'graph_thermal':
        return dcc.Graph(id='graph_thermal', figure=fig_thermal)
    elif selected_graph == 'graph_storage':
        return dcc.Graph(id='graph_storage', figure=fig_storage)
    elif selected_graph == 'graph_photovoltaic':
        return dcc.Graph(id='graph_photovoltaic', figure=fig_photovoltaic)
    elif selected_graph == 'graph_nuclear':
        return dcc.Graph(id='graph_nuclear', figure=fig_nuclear)
    elif selected_graph == 'graph_flow':
        return dcc.Graph(id='graph_flow', figure=fig_flow)
    elif selected_graph == 'graph_full':
        return dcc.Graph(id='graph_full', figure=fig_full)
    else:
        return None


# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
