#!/usr/bin python3

#import my_themes

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
import plotly.graph_objects as go
import math as math

df = pd.read_csv('data/kc_house_data.csv')

text_colors = 'rgb(0, 0, 0)'

colors = [
    '#02223c',
    '#FF0022',
    '#FF5C72',
    '#A0757B',
    '#41EAD4',
    '#0c6E61',
    '#FDFFFC',
    '#B91372',
    '#CFC0BD',
    '#586F6B',
    '#F2BB05',
    '#FFCF99'
]

# categorical_variables = ['bathrooms', 'floors', 'waterfront', 'view', 'condition', 'grade']

# Need to clean up how our date sold value is displayed.
def change_datetime(df, col):
    df[col] = df[col].apply(lambda x: x[:-7]).astype(int)
    df[col] = df[col].apply(lambda x: pd.to_datetime(x, format='%Y%m%d'))
    return df[col]

# creating a new year built column that will be by decade.
df['date_bin'] = df['yr_built']
df['date_bin'] = df['date_bin'].apply(lambda x: (math.floor(x/10) * 10))

# Need to change it to a string variable because when it's an integer it will think it's a continuous variable
# and not a categorical variable.
df['date_bin'] = df['date_bin'].astype(str)
cat_orders = ['1900', '1910', '1920', '1930', '1940', '1950', 
                '1960', '1970', '1980', '1990', '2000', '2010']

# we have one house with a number of bedrooms out at 33.
# this is a very big outlier that will skew all of our charts, so we are removing it.
df = df[df.bedrooms < 12]


df['date'] = change_datetime(df, 'date')

# Changing waterfront variable to a string so plotly knows it's categorical and not continous.
df['waterfront'] = df['waterfront'].astype(str)

external_stylesheets = [dbc.themes.DARKLY]


def getVariableFig(variable, df):
    df[variable] = df[variable].astype(str)
    df.sort_values('date_bin', ascending=True, ignore_index=True, inplace=True)
    df = df[df['price'] < 1500000]
    df = df[df['sqft_living'] < 4500]
    fig = px.scatter(
        df,
        x='sqft_living', 
        y='price', 
        color=variable, 
        animation_frame='date_bin',
        template='plotly_dark',
        color_discrete_sequence=colors
     )
    return fig

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': '#111111'},
    children=[
        html.H1(
            children="King's County Housing Data (2014 - 2015)",
            style={'textAlign':'center'}
            ),
        dcc.Markdown('''
            ### Select a categorical variable to see how the variable impacts the price.
            ''',
            style={'textAlign': 'center'}
        ),
       dcc.Graph(
            id='bedrooms',
            figure=getVariableFig('bedrooms', df)
        ),
        dcc.Graph(
            id='bathrooms',
            figure=getVariableFig('bathrooms', df)
         ),
        dcc.Graph(
            id='floors',
            figure=getVariableFig('bathrooms', df)
         ),
        dcc.Graph(
            id='waterfront',
            figure=getVariableFig('bathrooms', df)
         ),
        dcc.Graph(
            id='view',
            figure=getVariableFig('bathrooms', df)
         ),
        dcc.Graph(
            id='condition',
            figure=getVariableFig('bathrooms', df)
         ),
        dcc.Graph(
            id='grade',
            figure=getVariableFig('bathrooms', df)
         ),
        html.Div(
            children=[
                dbc.FormGroup(
                    [
                        dbc.RadioItems(
                    id='categorical-variables',
                    options=[
                        {'label': 'Bedrooms', 'value': 'bedrooms'},
                        {'label': 'Floors', 'value': 'floors'},
                        {'label': 'Bathrooms', 'value': 'bathrooms'},
                        {'label': 'Waterfront', 'value': 'waterfront'},
                        {'label': 'View', 'value': 'view'},
                        {'label': 'Condition', 'value': 'condition'},
                        {'label': 'Grade', 'value': 'grade'}
                    ],
                value='bedrooms',
                inline=True,
                style={'textAlign': 'center'
                     },
                    )
                ]
                ),
            ],
        ),
        html.Div(
            children=[
                html.Div(
                    dcc.Graph(
                        id='hist-variable'
                    ),
                        style={'display':'inline-block', 'width': '50%'}
                ),
                html.Div(
                    dcc.Graph(
                        id='hist-year'
                    ),
                        style={'display':'inline-block', 'width': '50%'}
                ),
            ],
        ),

        html.Div(
            dcc.Graph(
                id='hist-price'
            ),
        style={'width': '100%'}
        )
    ]
)
@app.callback(Output('bar', 'figure'),
        [Input('categorical-variables', 'value')])

def update_bar(val):
    df.sort_values('date_bin', ascending=True, ignore_index=True, inplace=True)
    df_new = df.groupby([val, 'date_bin'], as_index=False).mean()
    df_new[val] = df_new[val].astype(str)
    # In order to not show the observation lines for each value, we need to first group our data.
    fig = px.bar(
            df_new,
            x=val,
            y='price',
            template='plotly_dark',
            animation_frame='date_bin',
            #color='date_bin',
            barmode='group',
            #category_orders ={'date_bin': cat_orders},
            color_discrete_sequence=colors,
            range_y=[0, 1500000],
            range_x=[0,11]


        )
    fig.update_layout(
            title_text = 'Average Price Based on Variable Selected and Filtered by Year House was Built',
            xaxis_title = val,
            yaxis_title = 'Average Price',
        )

    return fig

@app.callback(Output('hist-variable', 'figure'),
        [Input('categorical-variables', 'value')])

def update_hist(val):
    fig = px.histogram(
            df,
            x=val,
            template='plotly_dark',
            histnorm='probability density',
            color_discrete_sequence=colors
        )
    fig.update_layout(
            title_text = f'Distribution of the {val} variables',
            xaxis_title = val,
            yaxis_title = 'Count of Occurence',
        )
    return fig

@app.callback(Output('hist-year', 'figure'),
        [Input('categorical-variables', 'value')])

def update_hist_year(val):
    fig = px.histogram(
            df,
            x='date_bin',
            color=val,
            template='plotly_dark',
            color_discrete_sequence=colors
        )
    fig.update_layout(
            title_text='Decade Distribution colored by each unique categorical variable selected',
            xaxis_title='Decade',
            yaxis_title='Count of Occurence'
        )
    return fig

@app.callback(Output('hist-price', 'figure'),
        [Input('categorical-variables', 'value')])

def update_hist_price(val):
    df_new = df[df['price'] < 5000000]
    # Filtered by less than 5 mil to eliminate some outliers so as to not clutter the histogram.
    fig = px.histogram(
            df_new,
            x='price',
            color=val,
            template='plotly_dark',
            color_discrete_sequence=colors

        )
    fig.update_layout(
            title_text='Price Distribution Colored by Unique Categorical Variable',
            xaxis_title='Price',
            yaxis_title='Count of Occurence',
        )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
