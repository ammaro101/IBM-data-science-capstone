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
launch_sites = spacex_df['Launch Site'].unique()
options = []
for i in launch_sites:
    option = {'label': i, 'value': i}
    options.append(option)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites',
                                                     'value': 'ALL'},
                                                 options[0],
                                                 options[1],
                                                 options[2],
                                                 options[3],
                                                #  {'label': launch_sites[0],
                                                #      'value': launch_sites[0]},
                                                #  {'label': launch_sites[1],
                                                #      'value': launch_sites[1]},
                                                #  {'label': launch_sites[2],
                                                #      'value': launch_sites[2]},
                                                #  {'label': launch_sites[3],
                                                #      'value': launch_sites[3]},
                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload, max=max_payload,
                                                marks={
                                                    min_payload: str(min_payload) + " KG",
                                                    max_payload/4: str(max_payload/4) + " KG",
                                                    max_payload/2: str(max_payload/2) + " KG",
                                                    max_payload*0.75: str(max_payload*0.75) + " KG",
                                                    max_payload: str(max_payload) + " KG"},
                                                step=1000,
                                                value=[min_payload, max_payload]),

                                # dcc.RangeSlider(id='payload-slider',
                                #                 min=0,
                                #                 max=10000,
                                #                 step=1000,
                                #                 value=[
                                #                     min_payload, max_payload]
                                #                 ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='title')
        return fig
    else:
        # return the outcomes piechart for a selected site

        # filtered_df = spacex_df.loc[spacex_df["Launch Site"]
        #                             == entered_site]
        # print(filtered_df)
        # fig = px.pie(filtered_df, values='class',
        #              names='class',
        #              title='title')

        # Filter the dataframe to include only data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Calculate success and failed counts for the selected site
        site_success = len(filtered_df.loc[filtered_df['class'] == 1])
        site_failed = len(filtered_df) - site_success
        fig = px.pie(values=[site_success, site_failed],
                     names=['Success', 'Failed'],
                     title='Success and Failed Launches at {}'.format(
                         entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site, payload_slider):

    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(
        payload_slider[0], payload_slider[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category')
        return fig
    else:
        # Filter the dataframe to include only data for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category')
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
