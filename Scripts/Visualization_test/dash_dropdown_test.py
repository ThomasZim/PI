import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

df_pc = pd.read_csv('../../Data/1hour_concat.csv', sep=',')
df_pc = df_pc.sort_values(by=['Date', 'Canton'])
df_pc = df_pc.reset_index(drop=True)
#Multiply consumption by -1 to get a negative value
df_pc['Consumption'] = df_pc['Consumption'] * -1

#Remove the rows with a production or consumption value of 0
df_pc = df_pc[df_pc.Production != 0]
df_pc = df_pc[df_pc.Consumption != 0]
#reindex the dataframe
df_pc = df_pc.reset_index(drop=True)

# pivot the DataFrame
df_pivot_prod = df_pc.pivot(index='Date', columns='Canton', values='Production').reset_index()
df_pivot_cons = df_pc.pivot(index='Date', columns='Canton', values='Consumption').reset_index()

colors = {
    'AG': 'rgb(255, 127, 14)',
    'AI/AR': 'rgb(44, 160, 44)',
    'BE/JU': 'rgb(31, 119, 180)',
    'BL/BS': 'rgb(214, 39, 40)',
    'FR': 'rgb(148, 103, 189)',
    'GE/VD': 'rgb(140, 86, 75)',
    'GL': 'rgb(227, 119, 194)',
    'GR': 'rgb(127, 127, 127)',
    'LU': 'rgb(188, 189, 34)',
    'NE': 'rgb(23, 190, 207)',
    'OW/NW/UR': 'rgb(174, 199, 232)',
    'SG': 'rgb(255, 187, 120)',
    'SH/ZH': 'rgb(152, 223, 138)',
    'SO': 'rgb(255, 152, 150)',
    'SZ/ZG': 'rgb(197, 176, 213)',
    'TG': 'rgb(196, 156, 148)',
    'TI': 'rgb(247, 182, 210)',
    'VS': 'rgb(199, 199, 199)'
}
#add _prod or _cons to the column names except for the date column
#df_pivot_prod.columns = ['Date'] + [str(col) + '_prod' for col in df_pivot_prod.columns[1:]]
#df_pivot_cons.columns = ['Date'] + [str(col) + '_cons' for col in df_pivot_cons.columns[1:]]


# create a Dash app
app = dash.Dash(__name__)

# create options for dropdown menus by using every unique value in the column 'Canton', do not use the date column
dropdown_options_prod = [{'label': x, 'value': x} for x in df_pivot_prod.columns[1:]]
dropdown_options_cons = [{'label': x, 'value': x} for x in df_pivot_cons.columns[1:]]

app.layout = html.Div([
    html.H1("Production and Consumption"),
    html.Div([
        html.Div([
            html.H3("Production"),
            dcc.Dropdown(
                id='prod-dropdown',
                options=dropdown_options_prod,
                value=['AG'],
                multi=True
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H3("Consumption"),
            dcc.Dropdown(
                id='cons-dropdown',
                options=dropdown_options_cons,
                value=['AG'],
                multi=True
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='graph'),
    html.Button('Toggle Prod-Cons Trace', id='toggle-button', n_clicks=0)
], style={'padding':10})

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('prod-dropdown', 'value'),
     dash.dependencies.Input('cons-dropdown', 'value'),
     dash.dependencies.Input('toggle-button', 'n_clicks')]
)
def update_figure(selected_prod_values, selected_cons_values, n_clicks):
    fig = go.Figure()
    # Create a trace for the total production - the total consumption
    if n_clicks % 2 == 0:
        show_trace = True
        fig.add_trace(go.Scatter(x=df_pivot_prod['Date'], y=df_pivot_prod[selected_prod_values].sum(axis=1) + df_pivot_cons[selected_cons_values].sum(axis=1), name='Total Production - Total Consumption', fill='tozeroy', line_color='dimgray'))
    else:
        show_trace = False
    
    # filter the DataFrame with selected values
    fig_prod = px.line(df_pivot_prod, x='Date', y=selected_prod_values, title='Production and Consumption', color_discrete_map=colors)
    fig_cons = px.line(df_pivot_cons, x='Date', y=selected_cons_values, title='Production and Consumption', color_discrete_map=colors)

    for data in fig_prod.data:
        fig.add_trace(data)
    for data in fig_cons.data:
        fig.add_trace(data)
    
    if not show_trace:
        fig.update_traces(visible=False, selector={'name':'Total Production - Total Consumption'})
    
    return fig



# run app
if __name__ == '__main__':
    app.run_server(debug=True)
