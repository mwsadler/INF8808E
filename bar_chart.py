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

def draw_pressure_viz(data, title, isChelsea):
    '''
        Draws the first viz: Rendement des pressions

        Arg:
            data: The data to be displayed.
            title: The title to display.
            isChelsea: True if the data is from Chelsea.
        Returns:
            fig: The figure including the drawn bar chart
    '''
    # TODO : Update the figure's data according to the selected mode
    colors = [
        '#33CCFF',
        '#FFC114',
    ]
    teamColor = ''
    if isChelsea:
        teamColor = '#034694' # Dark blue
    else:
        teamColor = '#6CADDF' # Light blue
    
    fig = go.Figure(data=[
        go.Bar(name='Reussi', x=data['Joueur'], y=data['PressionsReussis'], marker_color=teamColor),
        go.Bar(name='Rate', x=data['Joueur'], y=data['PressionsRate'], marker_color='#FFC114'),
    ])

    fig.update_layout(
        title_text=title,
        barmode='stack'
    )
    fig.update_xaxes(title_text = "Joueurs")
    fig.update_yaxes(title_text = "Nombre de pressions")
    
    return fig

def touches_viz(data):
    '''
        Draws the second viz: Touches par zone

        Arg:
            data: The data to be displayed.
        Returns:
            fig: The figure including the drawn centered stacked bar chart.
    '''
    colors = [
        '#6CADDF', # Light blue
        '#034694' # Dark blue
    ]

    fig = go.Figure(data=[
        go.Bar(name='Manchester City', x=-data['Man city'], y=data['Zone'], marker_color=colors[0], orientation='h',),
        go.Bar(name='Chelsea', x=data['Chelsea'], y=data['Zone'], marker_color=colors[1], orientation='h',),
    ])

    fig.update_layout(barmode='relative' )
    fig.update_xaxes(title_text = "Nombre de touches")
    fig.update_yaxes(title_text = "Zones")
    
    return fig

def passes_viz(data, title):
    '''
        Draws the third viz: Rendement des passes

        Arg:
            data: The data to be displayed.
            title: The title to display.
        Returns:
            fig: The figure including the drawn bar chart.
    '''
    colors = [
        '#90ee02', # Light green
        '#008b00', # Dark green
        '#FFFF00', # Light yellow
        '#FBC02D', # Dark yellow
        '#ee0290', # Light red
        '#880061', # Dark red
    ]
    
    fig = go.Figure(data=[
        go.Bar(name='Courtes Totales', x=data['Joueur'], y=data['CourtTot'], marker_color=colors[0], offsetgroup=0),
        go.Bar(name='Courtes Réussies', x=data['Joueur'], y=data['CourtReussis'], marker_color=colors[1], offsetgroup=0),
        go.Bar(name='Moyennes Totales', x=data['Joueur'], y=data['MoyenTot'], marker_color=colors[2], offsetgroup=1),
        go.Bar(name='Moyennes Réussies', x=data['Joueur'], y=data['MoyenReussis'], marker_color=colors[3], offsetgroup=1),
        go.Bar(name='Longues Totales', x=data['Joueur'], y=data['LongTot'], marker_color=colors[4], offsetgroup=2),
        go.Bar(name='Longues Réussies', x=data['Joueur'], y=data['LongReussis'], marker_color=colors[5], offsetgroup=2),
    ])

    fig.update_layout(
        title_text=title,
    )
    fig.update_xaxes(title_text = "Joueurs")
    fig.update_yaxes(title_text = "Nombre de passes")
    
    return fig

def shot_viz(dataChe, dataMan):
    '''
        Draws the forth viz: Tirs au cours du match

        Arg:
            dataChe: The data from Chelsea's team to be displayed.
            dataMan: The data from Manchester City's team to be displayed.
        Returns:
            fig: The figure including the drawn beeswarm plot.
    '''
    colors = [
        '#6CADDF', # Light blue
        '#034694' # Dark blue
    ]
    
    sizeref = 2.*max(dataMan['Distance'])/(100**2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataMan['Minute'], 
        y=dataMan['Resultat'],
        name='Manchester City',
        marker_size=dataMan['Distance'],
        marker_color=colors[0],
        ))
    fig.add_trace(go.Scatter(
        x=dataChe['Minute'], 
        y=dataChe['Resultat'],
        name='Chelsea',
        marker_size=dataChe['Distance'],
        marker_color=colors[1],
        ))

    fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                                sizeref=sizeref, line_width=2))

    fig.update_xaxes(title_text = "Minutes")
    fig.update_yaxes(title_text = "Résultats")

    return fig

def goaler_viz(dataChel, dataMan):
    '''
        Draws the fifth viz: Rendement des passes des gardiens

        Arg:
            dataChel: The data from Chelsea's team to be displayed.
            dataMan: The data from Manchester City's team to be displayed.
        Returns:
            fig: The figure including the drawn plot.
    '''
    pieColors = [
        '#E20000', # Red
        '#51E900' # Green
    ]

    shortPassChel = [dataChel['CourtRate'][0], dataChel['CourtReussis'][0]]
    longPassChel = [dataChel['LongRate'][0], dataChel['LongReussis'][0]]
    shortPassMan = [dataMan['CourtRate'][0], dataMan['CourtReussis'][0]]
    longPassMan = [dataMan['LongRate'][0], dataMan['LongReussis'][0]]
    labels = ["Raté", "Réussi"]

    fig = make_subplots(rows=2, cols=4,
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}, {"type": "domain"}],
                [{'colspan': 2}, None, {'colspan': 2}, None]])

    # Donuts Section
    fig.add_trace(go.Pie(labels=labels, values=shortPassChel, name="Edouard Mendy Court", marker_colors=pieColors),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=longPassChel, name="Edouard Mendy Long", marker_colors=pieColors),
                1, 2)
    fig.add_trace(go.Pie(labels=labels, values=shortPassMan, name="Ederson Court", marker_colors=pieColors),
                1, 3)
    fig.add_trace(go.Pie(labels=labels, values=longPassMan, name="Ederson Long", marker_colors=pieColors),
                1, 4)

    fig.update_traces(hole=.5, hoverinfo="label+percent+name") # Hole for the donut chart

    fig.update_layout(
        title_text="Rendement des passes des gardiens")

    # Bars Section
    fig.add_trace(go.Bar(
        y=['Edouard Mendy'],
        x=dataChel['TotalCourt'],
        name='Court',
        orientation='h',
        marker_color='#F6630D',
    ), 2, 1)
    fig.add_trace(go.Bar(
        y=['Edouard Mendy'],
        x=dataChel['TotalLong'],
        name='Long',
        orientation='h',
        marker_color='#FFC114',
    ), 2, 1)

    # Bars Section
    fig.add_trace(go.Bar(
        y=['Ederson'],
        x=dataMan['TotalCourt'],
        name='Court',
        orientation='h',
        marker_color='#F6630D',
    ), 2, 3)
    fig.add_trace(go.Bar(
        y=['Ederson'],
        x=dataMan['TotalLong'],
        name='Long',
        orientation='h',
        marker_color='#FFC114',
    ), 2, 3)

    fig.update_layout(barmode='stack')
    return fig
