'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
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


def draw(fig, data, mode):
    '''
        Ddrawraws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    fig.data = [] 

    # TODO : Update the figure's data according to the selected mode

    names = ['Benvolio', 'Juliet', 'Mercutio', 'Nurse', 'Others', 'Romeo']
    acts = ['Act 1','Act 2','Act 3','Act 4','Act 5']
    colors = [
        '#861388',
        '#d4a0a7',
        '#dbd053',
        '#1b998b',
        '#A0CED9',
        '#3e6680'
    ]
    
    modeIndex = 3
    lines = []
    if(mode == 'Count'):
        modeIndex = 2

    
    i = 0
    for name in names:
        templateItem = hover_template.get_hover_template(name, mode)
        temp = data.loc[data['Player'].isin([name])].to_numpy()
        tempLine = [0] * 5
        for item in temp:
            tempLine[item[1] - 1] = item[modeIndex]
        lines.append(tempLine)
        fig.add_trace(go.Bar(name=name, x=acts, y=lines[i], marker_color=colors[i], hovertemplate = templateItem))
        i += 1

    
    
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