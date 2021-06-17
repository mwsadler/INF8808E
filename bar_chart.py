'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots

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

def touches_viz(fig, data):
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
    colors = [
        '#861388',
        '#d4a0a7'
    ]
    
    fig = go.Figure(data=[
        go.Bar(name='Manchester City', x=-data['Man city'], y=data['Zone'], marker_color=colors[0], orientation='h',),
        go.Bar(name='Chelsea', x=data['Chelsea'], y=data['Zone'], marker_color=colors[1], orientation='h',),
    ])

    #fig.update_layout(barmode='stack')
    fig.update_layout(barmode='relative'
                 )
    
    return fig

def passes_viz(fig, data):
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
    colors = [
        '#861388',
        '#d4a0a7',
        '#dbd053',
        '#1b998b',
        '#A0CED9',
        '#3e6680'
    ]
    
    fig = go.Figure(data=[
        go.Bar(name='Courtes Réussies', x=data['Joueur'], y=data['CourtReussis'], marker_color=colors[0], offsetgroup=0),
        go.Bar(name='Courtes Ratées', x=data['Joueur'], y=data['CourtRate'], marker_color=colors[1], offsetgroup=0),
        go.Bar(name='Moyennes Réussies', x=data['Joueur'], y=data['MoyenReussis'], marker_color=colors[2], offsetgroup=1),
        go.Bar(name='Moyennes Ratées', x=data['Joueur'], y=data['MoyenRate'], marker_color=colors[3], offsetgroup=1),
        go.Bar(name='Longues Réussies', x=data['Joueur'], y=data['LongReussis'], marker_color=colors[4], offsetgroup=2),
        go.Bar(name='Longues Ratées', x=data['Joueur'], y=data['LongRate'], marker_color=colors[5], offsetgroup=2),
    ])

    #fig.update_layout(barmode='stack')
    
    return fig

def shot_viz(fig, data):
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
    colors = [
        '#861388',
        '#d4a0a7',
        '#dbd053',
        '#1b998b',
        '#A0CED9',
        '#3e6680'
    ]
    
    # fig = go.Figure(data=go.Scatter(
    #     x=data['Time'],
    #     y=data['But'],
    #     mode='markers',
    #     marker=dict(size=data['Distance'],
    #                 color=[0, 1, 2, 3])
    # ))
    sizeref = 2.*max(data['Distance'])/(100**2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Time'], 
        y=data['But'],
        name='Manchester City',
        marker_size=data['Distance'],
        ))
    fig.add_trace(go.Scatter(
        x=data['Time'], 
        y=data['But'],
        name='Chelsea',
        marker_size=data['Distance'],
        ))
    # Tune marker appearance and layout
    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                sizeref=sizeref, line_width=2))
    #fig.update_layout(barmode='stack')
    
    return fig

def goaler_viz(fig, data):
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

    labels = ["Raté", "Réussi"]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=data['GoalerAShort'], name="GoalerAShort"),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=data['GoalerALong'], name="GoalerALong"),
                1, 2)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="Rendement des passes des gardiens",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Court', x=0.18, y=0.5, font_size=20, showarrow=False),
                    dict(text='Long', x=0.82, y=0.5, font_size=20, showarrow=False)])
    

    # Bars Section
    fig.add_trace(go.Bar(
        y=['GoalerA'],
        x=data['GoalerAShortRatio'],
        name='Court',
        orientation='h',
        marker=dict(
            color='rgba(246, 78, 139, 0.6)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        ),
    ), 2, 1)
    fig.add_trace(go.Bar(
        y=['GoalerA', 'orangutans', 'monkeys'],
        x=data['GoalerALongRatio'],
        name='Long',
        orientation='h',
        marker=dict(
            color='rgba(58, 71, 80, 0.6)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
        )
    ), 2, 1)

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