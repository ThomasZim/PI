import dash
from dash import dcc
from dash  import html
import pandas as pd
import matplotlib as plty
import plotly.express as px

#Open dataset
df = pd.read_csv('../../Data/ogd104_stromproduktion_swissgrid.csv', sep=',')

# Open EletricityProductionPlant dataset
df_plants = pd.read_csv('../../Data/ElectricityProductionPlant.csv', sep=',')

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

fig_ch = px.scatter_mapbox(df_plants, lat="lat", lon="lon", hover_name="Municipality", zoom=7)
fig_ch.update_layout(mapbox_style="carto-positron",
                  mapbox_center={"lat": 46.8182, "lon": 8.2275},
                  mapbox_zoom=6)

#Create a new dataframe for every different type of energy
df_wind = df[df['Energietraeger'] == 'Wind']
df_thermal = df[df['Energietraeger'] == 'Thermische']
df_storage = df[df['Energietraeger'] == 'Speicherkraft']
df_photovoltaic = df[df['Energietraeger'] == 'Photovoltaik']
df_nuclear = df[df['Energietraeger'] == 'Kernkraft']
df_flow = df[df['Energietraeger'] == 'Flusskraft']

#Translate the german names to english
df_thermal = df_thermal.rename(columns={'Thermische': 'Thermal'})
df_storage = df_storage.rename(columns={'Speicherkraft': 'Storage'})
df_photovoltaic = df_photovoltaic.rename(columns={'Photovoltaik': 'Photovoltaic'})
df_nuclear = df_nuclear.rename(columns={'Kernkraft': 'Nuclear'})
df_flow = df_flow.rename(columns={'Flusskraft': 'Flow'})

#Sort the dataframes by date
df_wind = df_wind.sort_values(by=['Datum'])
df_thermal = df_thermal.sort_values(by=['Datum'])
df_storage = df_storage.sort_values(by=['Datum'])
df_photovoltaic = df_photovoltaic.sort_values(by=['Datum'])
df_nuclear = df_nuclear.sort_values(by=['Datum'])
df_flow = df_flow.sort_values(by=['Datum'])

#Create figs for every dataframe
fig_wind = px.line(df_wind, x='Datum', y='Produktion_GWh', title='Wind Production in Switzerland')
fig_wind.update_xaxes(title_text='Date')
fig_wind.update_yaxes(title_text='Production (GWh)')

fig_thermal = px.line(df_thermal, x='Datum', y='Produktion_GWh', title='Thermal Production in Switzerland')
fig_thermal.update_xaxes(title_text='Date')
fig_thermal.update_yaxes(title_text='Production (GWh)')

fig_storage = px.line(df_storage, x='Datum', y='Produktion_GWh', title='Storage Production in Switzerland')
fig_storage.update_xaxes(title_text='Date')
fig_storage.update_yaxes(title_text='Production (GWh)')

fig_photovoltaic = px.line(df_photovoltaic, x='Datum', y='Produktion_GWh', title='Photovoltaic Production in Switzerland')
fig_photovoltaic.update_xaxes(title_text='Date')
fig_photovoltaic.update_yaxes(title_text='Production (GWh)')

fig_nuclear = px.line(df_nuclear, x='Datum', y='Produktion_GWh', title='Nuclear Production in Switzerland')
fig_nuclear.update_xaxes(title_text='Date')
fig_nuclear.update_yaxes(title_text='Production (GWh)')

fig_flow = px.line(df_flow, x='Datum', y='Produktion_GWh', title='Flow Production in Switzerland')
fig_flow.update_xaxes(title_text='Date')
fig_flow.update_yaxes(title_text='Production (GWh)')

df_full = pd.concat([df_wind, df_thermal, df_storage, df_photovoltaic, df_nuclear, df_flow])
fig_full = px.line(df_full, x='Datum', y='Produktion_GWh', color='Energietraeger', title='Energy Production in Switzerland')
fig_full.update_xaxes(title_text='Date')
fig_full.update_yaxes(title_text='Production (GWh)')

#Create a dataframe with 

# Initialize the app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    # Display the map
    dcc.Graph(id='graph_ch', figure=fig_ch),

    # Display the wind dataframe
    dcc.Graph(id='graph_wind', figure=fig_wind),

    # Display the thermal dataframe
    dcc.Graph(id='graph_thermal', figure=fig_thermal),

    # Display the storage dataframe
    dcc.Graph(id='graph_storage', figure=fig_storage),

    # Display the photovoltaic dataframe
    dcc.Graph(id='graph_photovoltaic', figure=fig_photovoltaic),

    # Display the nuclear dataframe
    dcc.Graph(id='graph_nuclear', figure=fig_nuclear),

    # Display the flow dataframe
    dcc.Graph(id='graph_flow', figure=fig_flow),

    # Display the full dataframe
    dcc.Graph(id='graph_full', figure = fig_full)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
