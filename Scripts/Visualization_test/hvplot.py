import pandas as pd
import panel as pn
import hvplot.pandas  

#Open dataset
df = pd.read_csv('../../Data/ogd104_stromproduktion_swissgrid.csv', sep=',')

#Create a new dataframe for every different type of energy
df_wind = df[df['Energietraeger'] == 'Wind']
df_thermal = df[df['Energietraeger'] == 'Thermische']
df_storage = df[df['Energietraeger'] == 'Speicherkraft']
df_photovoltaic = df[df['Energietraeger'] == 'Photovoltaik']
df_nuclear = df[df['Energietraeger'] == 'Kernkraft']
df_flow = df[df['Energietraeger'] == 'Flusskraft']

#Reindex the dataframes
df_wind = df_wind.reset_index(drop=True)
df_wind.head()

#Make sure every dataframe length added up is equal to the original dataframe
print(len(df_wind) + len(df_thermal) + len(df_storage) + len(df_photovoltaic) + len(df_nuclear) + len(df_flow))
print(len(df))

# Create Selector (widget) containing all possible energy types
energy_types = list(df.Energietraeger.unique())
energy_type = pn.widgets.Select(name='Type', options=energy_types)

# Define function to filter data and create plot
@pn.depends(energy_type.param.value)
def plot_energy_production(energy_type_value):
    print('energy_type_value:', energy_type_value)
    df_filtered = df[df['Energietraeger'] == energy_type_value]
    plot = df_filtered.hvplot.line(x='Datum', y='Produktion_GWh', grid=True, title=f'Energy production for {energy_type_value}')
    return plot

# Combine widget and plot into a dashboard
dashboard = pn.Column(energy_type, plot_energy_production)

# Print the widget to see if it's being displayed correctly
print(energy_type)

# Launch the dashboard
dashboard.servable()