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
        '#375a7f', #blue 0
        '#6610f2', #indigo 1
        '#6f42c1', #purple 2
        '#e83e8c', #pink 3
        '#E74C3C', #red 4
        '#fd7e14', #orange 5
        '#F39C12', #yellow 6
        '#00bc8c', #green 7
        '#20c997', #teal 8
        '#3498DB'  #cyan 9
    ]

def change_datetime(df, col):
    df[col] = df[col].apply(lambda x: x[:-7]).astype(int)
    df[col] = df[col].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
    return df[col]

df['date'] = change_datetime(df, 'date')

# df = df[df['bedrooms'] < 3]

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
        ),
        html.Div(
            children=[
                html.H1(
                    children='Please Enter the Number of Bedrooms',
                    style={'textAlign': 'center'}
                ),
                dcc.Input(
                    id='bedrooms',
                    type='number',
                    debounce=True,
                    value=1,
                    placeholder=1,
                    style={
                        'backgroundColor': 'rgb(-1,0,0)',
                        'color': colors[7],
                        'textAlign':'center'
                    },            
                    
                ),
            ],
            style={'textAlign':'center'}
        )
    ]
)
            

@app.callback(Output('sqft_living vs sqft_lot', 'figure'),
        [Input('bedrooms', 'value')])
def update_scatter(val):
    df1 = df[df['bedrooms'] == val]
    s = px.scatter(
            df1,
            x='date',
            y='price',
            size='sqft_living',
            template='plotly_dark',
            color='floors',
            title='Price Over Time and Coloured by # of Bedrooms'
    )
    s.update_layout(
            font_family="Rockwell"
    )
    return s


if __name__ == '__main__':
    app.run_server(debug=True)
