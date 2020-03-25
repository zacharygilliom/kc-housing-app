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
df['waterfront'] = df['waterfront'].astype(str)
df_bar_group = df[df.bedrooms < 30].groupby(['bedrooms'], as_index=False).mean() 
# df_wat_bed_group = df[df[.bedrooms < 30].groupby(['waterfront'], as_index=False).mean()

# print(df.columns)
# print(list(df['bedrooms'].unique()))
external_stylesheets = [dbc.themes.DARKLY]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(
            children="King's County Housing Data (2014 - 2015)",
            style={'textAlign':'center'}
            ),
        dcc.Markdown('''
            ### Let's take a look at how the number of bedrooms in a house has impacted the price of the house.
            '''
        ),
        html.Div(
            children=[
                html.H3(
                    children='Please Enter the Number of Bedrooms',
                    style={'textAlign': 'center',
                    }
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
        ),
        dcc.Graph(
            id='waterfront_bar_graph',
            figure=px.bar(
                df_bar_group,
                x='bedrooms',
                y='price',
                # color='waterfront',
                barmode='group',
                template='plotly_dark'
            )
        ),

        html.Div(
            children=[
                dcc.Graph(
                #TODO Need to style this bargraph to show some more important data
                    id='bar-graph'
                )
            ]
        ),
        html.Div(
            children=[
                dcc.Graph(
                    #TODO Fix this graph so we can look at some other factors.
                    id='line-graph-bedrooms'
                )
            ]
        )
    ]
)
@app.callback(Output('bar-graph', 'figure'),
        [Input('bedrooms', 'value')])
def update_bar(val):
    df2 = df.copy()
    df2 = df2.loc[df2.bedrooms ==val]
    df2['floors'] = df2['floors'].astype(str)
    df3 = df2.groupby(['floors', 'date'], as_index=False).mean()
    f = px.bar(
            df3,
            x='date',
            y='price',
            color='floors',
            barmode='stack',
            template='plotly_dark'
        )
    f.update_layout(
            title='Year House Built Grouped By Number of Floors',
            bargap=0.15,
            bargroupgap=0.05
        )
    return f

@app.callback(Output('line-graph-bedrooms', 'figure'),
        [Input('bedrooms','value')])

def update_line(val):
    # TODO Need to make this graph look better.  What are some other factors we can look at that impact the price?? 
    df_wat_bed_group = df[df.bedrooms < 30].groupby(['waterfront', 'date'], as_index=False).mean()
    df_wat_bed_group = df_wat_bed_group.loc[df_wat_bed_group.bedrooms == val]
    j = px.bar(
           df_wat_bed_group,
           x='date',
           y='price',
           color='waterfront',
           template='plotly_dark',
           barmode='group'
        )


    return j

if __name__ == '__main__':
    app.run_server(debug=True)
    # app.scripts.config.serve_locally = True
    # app.css.config.serve_locally = True
