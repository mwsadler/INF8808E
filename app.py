
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd

import preprocess
import bar_chart

from template import create_template
from modes import MODES


app = dash.Dash(__name__)
app.title = 'TP2 | INF8808'


def prep_data_poss():
    dfPossChel= pd.read_csv('./assets/data/PossessionChelsea.csv') #2 
    dfPossMan = pd.read_csv('./assets/data/PossessionManCity.csv') #2 
    proc_data = preprocess.clean_poss(dfPossChel, dfPossMan)
    return proc_data

def prep_data_pass():
    dfPasseChel = pd.read_csv('./assets/data/TypesDePasseChelsea.csv') #3
    dfPasseMan = pd.read_csv('./assets/data/TypesDePasseManCity.csv') #3

    proc_data_man = preprocess.clean_pass(dfPasseMan)
    proc_data_chel = preprocess.clean_pass(dfPasseChel)
    return proc_data_chel, proc_data_man

def prep_data_shot():
    dfTirs = pd.read_csv('./assets/data/Tirs.csv')  #4

    proc_data = preprocess.clean_shot(dfTirs)
    return proc_data

def prep_data_goaler():
    dfGardienChel = pd.read_csv('./assets/data/TypesDePasseChelsea.csv') #5
    dfGardienMan = pd.read_csv('./assets/data/TypesDePasseManCity.csv') #5

    proc_data_man = preprocess.clean_goaler(dfGardienMan)
    proc_data_chel = preprocess.clean_goaler(dfGardienChel)
    return proc_data_chel, proc_data_man

def prep_data_press():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    dfDefManCity = pd.read_csv('./assets/data/ActionDefensiveManCity.csv') #1 
    dfDefChel = pd.read_csv('./assets/data/ActionDefensiveChelsea.csv') #1 
    
    proc_data_man = preprocess.clean_pressure(dfDefManCity)
    proc_data_chel = preprocess.clean_pressure(dfDefChel)
    return proc_data_chel, proc_data_man


def init_app_layout(figPressureChel, figPressureMan, figPoss, figPassChel, figPassMan, figure):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Finale ligue des champion 2020-2021: Manchester city vs chelsea'),
            html.H2('Analyse des performances des 2 équipes')
        ]),
        html.Main(children=[
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 1: Pressions'),
                html.Div('Blablablablabalbla')
            ]),
            html.Div(className='viz-comparison', children=[
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=figPressureChel,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='v1-1'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=figPressureMan,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='v1-2'
                    )
                ]),
            ]),
            
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 2: Touches par zone'),
                html.Div('Blablablablabalbla')
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figPoss,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v2'
                )
            ]),
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 3: Rendement des passes'),
                html.Div('Blablablablabalbla')
            ]),
            html.Div(className='viz-comparison', children=[
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=figPassChel,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='v3-1'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=figPassMan,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='v3-2'
                    )
                ]),
            ]),
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 4: Tirs au cours du match'),
                html.Div('Blablablablabalbla')
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figure,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v4'
                )
            ]),
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 5: Rendement des passes des gardiens'),
                html.Div('Blablablablabalbla')
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figure,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='v5'
                )
            ]),
        ]),
    ])
    

data_press_viz_chel, data_press_viz_man = prep_data_press()
data_pass_viz_chel, data_pass_viz_man = prep_data_pass()
data_poss_viz = prep_data_poss()
data_shot_viz = prep_data_shot()
data_goaler_viz = prep_data_goaler()
create_template()

fig = bar_chart.init_figure()

figPressureChel = bar_chart.draw_pressure_viz(fig, data_press_viz_chel)
figPressureMan = bar_chart.draw_pressure_viz(fig, data_press_viz_man)

figPoss = bar_chart.touches_viz(fig, data_poss_viz)

figPassChel = bar_chart.passes_viz(fig, data_pass_viz_chel)
figPassMan = bar_chart.passes_viz(fig, data_pass_viz_man)

app.layout = init_app_layout(figPressureChel, figPressureMan, figPoss, figPassChel, figPassMan, figPressureMan)