import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import numpy as np
import dash_table as dt
import plotly.io as pio
import plotly.express as px
from dash.dependencies import Input, Output



df = pd.read_csv('data/kc_house_data.csv')

text_colors = 'rgb(0, 0, 0)'
colors = [
        '#375a7f', #blue
        '#6610f2', #indigo
        '#6f42c1', #purple
        '#e83e8c', #pink
        '#E74C3C', #red
        '#fd7e14', #orange
        '#F39C12', #yellow
        '#00bc8c', #green
        '#20c997', #teal
        '#3498DB'  #cyan
    ]

def change_datetime(df, col):
    df[col] = df[col].apply(lambda x: x[:-7]).astype(int)
    df[col] = df[col].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
    return df[col]

df['date'] = change_datetime(df, 'date')

df = df[df['bedrooms'] < 3]

print(df.columns)
print(list(df['bedrooms'].unique()))
external_stylesheets = [dbc.themes.DARKLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(
            children="King's County Housing Data (2014 - 2015)",
            style={'textAlign':'center'}
            ),
        dcc.Graph(
            id='sqft_living vs sqft_lot',
            figure=px.scatter(
                df,
                x='date',
                y='price',
                size='sqft_living',
                template='plotly_dark',
                color='floors',
                title='Price overtime and colored by # of bedrooms'
            )
                                
                

            )
            
        ]
        
        
        
    )

if __name__ == '__main__':
    app.run_server(debug=True)
