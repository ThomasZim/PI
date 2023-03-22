import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import pyproj

# df =  pd.read_csv("/home/mathu/Documents/pi/PI/Data/ogd104_stromproduktion_swissgrid.csv")
# dates = sorted(df["Datum"].unique())
# energy_types = sorted(df["Energietraeger"].unique())
# Valeur =  df["Produktion_GWh"]
# selected_date = st.selectbox("Sélectionnez une date", dates)
# selected_energy = st.selectbox("Sélectionnez un type d'énergie", energy_types)

# filtered_data = df[(df["Datum"] == selected_date) & (df["Energietraeger"] == selected_energy)]
# data_energy = df[(df["Energietraeger"] == selected_energy)]

# st.title("Données filtrées")
# st.write(filtered_data)

# st.title("Graphiques de la production d'énergie en fonction du type d'énergie")
# st.line_chart(data=data_energy,x="Datum", y="Produktion_GWh", )

# fig = px.bar(data_energy, x="Datum", y="Produktion_GWh",color="Energietraeger")

# st.plotly_chart(fig)

# lire le fichier csv
df_plants = pd.read_csv('../../../Data/ElectricityProductionPlant.csv', sep=',')

# Remove all the rows that have a NaN value
df_plants = df_plants.dropna()

# Open cords_WGS84.csv
df_cords_WGS84 = pd.read_csv('../../../Data/cords_WGS84.csv', sep=',')

# Add the coordinates to the original dataframe
df_plants['y_WGS84'] = df_cords_WGS84['lat']
df_plants['x_WGS84'] = df_cords_WGS84['lon']


# afficher les colonnes de latitude et longitude
st.write(df_plants[["x_WGS84", "y_WGS84"]])

fig = px.scatter_mapbox(df_plants, lat="x_WGS84", lon="y_WGS84", hover_name="Municipality", zoom=7)
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_center={"lat": 46.8182, "lon": 8.2275},
                  mapbox_zoom=6)


# # afficher la carte dans l'interface Streamlit
st.plotly_chart(fig)