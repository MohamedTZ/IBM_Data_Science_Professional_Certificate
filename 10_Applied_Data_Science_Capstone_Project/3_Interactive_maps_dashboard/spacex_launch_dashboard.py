# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = ['All sites', 'CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E'], value='All sites', placeholder = 'Select a Launch Site here', searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                                marks={0:'0', 2500:'2500', 5000:'5000', 7500:'7500', 10000:'10000'},
                                                value=[min_payload, max_payload], 
                                                tooltip={'placement':'bottom', 'always_visible':True, 
                                                         'style':{'color':'LightSteelBlue', 'fontSize':'20px'}}),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ]
                    )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'All sites':
        filtered_df = spacex_df[spacex_df['class']==1].groupby(['Launch Site'], as_index=False)['class'].count()
        fig = px.pie(filtered_df, values = 'class', names='Launch Site', 
                     title='Total Success Launches By Site', 
                     color_discrete_sequence= ['cyan', 'green', 'blue', 'yellow'])
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site].groupby(['class'], as_index=False)['class'].count()
        filtered_df.reset_index(inplace=True)
        filtered_df.columns = ['class', 'count'] 
        fig = px.pie(filtered_df, values= 'count', names= 'class',
                     title = f'Total Success Launches by {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_graph(entered_site, payload_mass):
    #Input(component_id='payload-slider', component_property='value'): This line connects the value of the payload slider
    # to the payload_mass argument of the get_payload_chart function. #When the user changes the slider, 
    # the selected range (a list of two values [min_value, max_value]) is passed as payload_mass to the callback function.
    
    

    if entered_site == 'All sites':
        scatter_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_mass[0]) & (spacex_df['Payload Mass (kg)'] <= payload_mass[1])]
        fig = px.scatter(scatter_df, 
                         x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', title='Payload and Launch outcome for all Sites')
        return fig
        
    else:
        scatter_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(scatter_df, 
                         x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f'Payload and Launch outcome for {entered_site}')
        
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

#1) Which site has the largest successful launches?
# CCAFS LC-40 and KSC LC-39A have 10 successful launches each.

#2) Which site has the highest launch success rate?
# KSC LC-39A has the hightest launch success rate at 76.9% (10 successful out of 13)

#3) Which payload range(s) has the highest launch success rate?
# 2000 - 3700 range has highest launch success rate

#4) Which payload range(s) has the lowest launch success rate?
# From the dataset provided, ranges between 500 - 2000 kg, 4000 - 4500 kg and 5500 - 9500 kg have the lowest success rate.

#5) Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?  
# FT booster has 100% launch success rate.
