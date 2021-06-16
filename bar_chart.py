'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

import hover_template
from modes import MODES, MODE_TO_COLUMN


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()

    # plotly_template = pio.templates["simple_white"]
    # print (plotly_template)
    # TODO : Update the template to include our new theme and set the title
    fig.update_layout(
        template=pio.templates['custom'],
        dragmode=False,
        barmode='relative',
        title=go.layout.Title(text="Lines per act")
    )

    return fig


def draw_pressure_viz(fig, data):
    '''
        Ddrawraws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    # TODO : Update the figure's data according to the selected mode

    traces = ['Total', 'Reussi']
    names = data['Joueur'].unique()
    colors = [
        '#861388',
        '#d4a0a7',
    ]
    
    fig = go.Figure(data=[
        go.Bar(name='Reussi', x=data['Joueur'], y=data['PressionsReussis']),
        go.Bar(name='Rate', x=data['Joueur'], y=data['PressionsRate']),
    ])

    fig.update_layout(barmode='stack')
    
    return fig


def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    title = "Lines (%)"
    if mode == "Count":
        title = "Lines (Count)"
    fig.update_layout(
        yaxis_title=title,
    )
    return fig