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
df = pd.read_csv("../../../Data/ElectricityProductionPlant.csv", sep=",")

# extraire les colonnes x et y
x = df["x"]
y = df["y"]

# définir le système de coordonnées d'origine (Swissgrid)
crs_swissgrid = pyproj.CRS.from_epsg(21781)

# définir le système de coordonnées de destination (WGS84)
crs_wgs84 = pyproj.CRS.from_epsg(4326)

# créer un transformateur de coordonnées de Swissgrid à WGS84
transformer = pyproj.Transformer.from_crs(crs_swissgrid, crs_wgs84, always_xy=True)

# appliquer la transformation de coordonnées à tous les points
lon, lat = transformer.transform(x.values, y.values)

# ajouter les coordonnées géographiques au DataFrame
df["latitude"] = lat
df["longitude"] = lon

# afficher les colonnes de latitude et longitude
st.write(df[["latitude", "longitude"]])

# charger les données géographiques de la Suisse depuis geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
switzerland = world[world.name == 'Switzerland']
print(switzerland)

# créer la carte avec Plotly
fig = px.choropleth_mapbox(switzerland, geojson=switzerland.geometry, hover_name='name',
                           center={"lat": 46.8, "lon": 8.2}, mapbox_style="carto-positron", zoom=6)

# afficher la carte dans l'interface Streamlit
st.plotly_chart(fig)