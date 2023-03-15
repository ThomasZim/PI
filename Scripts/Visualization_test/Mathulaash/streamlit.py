import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df =  pd.read_csv("/home/mathu/Documents/pi/PI/Data/ogd104_stromproduktion_swissgrid.csv")
dates = sorted(df["Datum"].unique())
energy_types = sorted(df["Energietraeger"].unique())
Valeur =  df["Produktion_GWh"]
selected_date = st.selectbox("Sélectionnez une date", dates)
selected_energy = st.selectbox("Sélectionnez un type d'énergie", energy_types)

filtered_data = df[(df["Datum"] == selected_date) & (df["Energietraeger"] == selected_energy)]
data_energy = df[(df["Energietraeger"] == selected_energy)]

st.title("Données filtrées")
st.write(filtered_data)

st.title("Graphiques de la production d'énergie en fonction du type d'énergie")
st.line_chart(data=data_energy,x="Datum", y="Produktion_GWh", )

fig = px.bar(data_energy, x="Datum", y="Produktion_GWh",color="Energietraeger")

st.plotly_chart(fig)
