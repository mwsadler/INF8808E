
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Félix Dumont, Augustin Bouchard, Mark Weber-Sadler
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
server = app.server
app.title = 'ProjetFinal | INF8808'

# Data pre-process
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

    proc_data_chel,  proc_data_man= preprocess.clean_shot(dfTirs)
    return proc_data_chel, proc_data_man

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

def init_app_layout(figPressureChel, figPressureMan, figPoss, figPassChel, figPassMan, figShots, figGoalers):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Finale de la ligue des champions du 29 Mai 2021: Manchester city vs chelsea'),
            html.H2("Analyse des performances des 2 équipes lors du match qui s'est solder par la marque de 1-0 pour Chelsea.")
        ]),
        html.Main(children=[
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 1: Pressions défensives'),
                html.Div(
                    '''
                        Les graphiques ci-dessous présente les pressions défensives réussis sur le total de pressions effectuées pour chaque joueur des 2 équipe.
                        Les joueurs sont en ordre de ceux qui ont fait les plus de pressions à ceux qui en ont fait le moins.
                        Les barres sont représenté ainsi pour permettre à l'entraineur de voir la performance individuelle de chacun de ces joueurs en terme de pressions défensives.
                        Pour l'équipe de Chelsea, on voit que Jorghino et Ben Chilwell ont eu un grand nombre de touches et qu'ils ont raté la grande majorité de leur pressions défensive. 
                        Ce serait alors à l'avantage de l'équipe si ces joueurs pratiquait leurs pressions défensive à l'entrainement.
                        En comparant les deux équipes, nous pouvons voir que l'équipe Chelsea a, en général un meilleur ratio de pressions défensives réussis que Manchester City.
                    '''
                )
            ]), 
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
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 2: Touches par zone'),
                html.Div(
                    '''
                        Le graphique ci-dessous nous montre le nombre de touche de chacune des équipes classé par la zone dans laquelle elles ont été faites. 
                        Cela nous permet de voir quelle équipe garde le controle du ballon et si une équipe est plus sur la défensive ou sur l'offensive. 
                        Pour voir qu'elle équipe performe le mieux durant le match, nous pouvons regarder quelle équipe a le plus de touche dans les zones offensives et centrale, et le moins de touche dans la zone défensive.
                        Pour la partie opposant Chelsea à Manchester City, nous pouvons déterminer que Manchester City domine la zone offensive et centrale, donc a un meilleur controle de la partie que Chelsea.
                        Chelsea a plus de touche en zone défensive ce qui veut surement indiqué qu'ils jouait beaucoup dans leur zone de terrain, donc n'était pas une menace pour l'opposant.
                        Cette analyse nous montre aussi que ce n'est pas l'équipe qui controle le jeu qui gagne necessairement la partie, car malgré tout Chelsea a remporter la partie.
                        Cela indique que Manchester City n'a pas eu la finission qu'ils auraient espérer.
                    '''
                )
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
                html.Div(
                    '''
                        Les visualisation ci-dessous sur le rendement des passes présente le ratio des passes réussies et des passes raté pour les 3 types de passes soit courte, moyenne et longue.
                        Pour chacune des équipe, il y a un graphique présentant le rendement despasses pour chacun de ces joueurs en ordre de ceux qui ont fait le plus de passe total.
                        Ces visualisations permettent de voir quels types de passe sont le plus réussis et raté pour prevoir le prochain entrainnement des équipes.
                        La légende permet de retirer certaines données pour plus de lisibilité au besoin.
                        Nous pouvons aussi comparer le style de jeu des deux équipes.
                        Les joueurs de Manchester City ont effectué et réussis beaucoup plus de passe moyenne que Chelsea, donc on peut déterminer que Manchester City jouait un jeu moins compact que Chelsea et dominait plus la partie.
                        
                    '''
                )
            ]),
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
            html.Div(className='viz-info', children=[
                html.H1('Visualisation 4: Tirs au cours du match'),
                html.Div(
                    '''
                        Le graphique ci-dessous nous montre un sommaire du match selon en fonction des tirs aux buts.
                        Il montre les 3 différents résultats de tir, soit un but, un tir cadré ou un tir non-cadré.
                        On voit aussi la distance du tir selon le rayon de chaque bulle, donc plus une bulle est grosse, plus le tir est effectué de loin.
                        Avec ces données, il est clair pour un entrainneur de voir l'allure de la partie en fonction du temps et de voir les opportunités de but.
                        Il est clair que Chelsea a gagné, car elle a eu le seul but de la partie, mais Manchester City avait plus de tirs cadré. 
                        Cela peut indiquer plus information aux entraineurs des 2 équipes.
                        Pour Chelsea, il y a un manque à la défense qui laisse beaucoup de tirs, le gardien à joué une bonne partie et à l'attaque les joueurs n'ont pas eu beaucoup de tir cadré, mais ils en ont réussis un.
                        Pour Manchester City, la défense a effectuer un bon travail d'empecher les tirs cadré, le gardien n'a pas eu une bonne partie, car il un mauvais ratio d'arrêts, et en attaque ils ont eu une bonne partie avec beaucoup de tir cadré , mais un manque de finition.
                    '''
                )
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figShots,
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
                html.Div(
                    '''
                        Le graphique ci-dessous nous montre plusieurs information à propos des passes du gardien.
                        Les graphiques en beignet nous montre la complétion des passes du gardien soit pour les passes de courte distance et les passes de longues distance.
                        Le bar chart nous montre la quantité de passes coutes en relation avec le nombre de passes longues.
                        Dans la section des passes courtes les deux gardiens ont réussi toutes leurs passes.
                        Dans la section des passes longues, le gardien de Chelsea a réussis environ le 2/3 de ses passe et le gardien de Manchester City seulement le 1/3.
                        Finalement, il est possible de voir que pour le gardien de Chelsea a fait beaucoup plus de passe longue que l'autre gardien.
                        Le gardien de Manchester City, lui, a fait une majorité de passe courte.
                        Cela démontre le type de jeu que chaque équipe jouait. 
                        Chelsea se faisait dominer, donc le gardien voulais sortir le ballon le plus de sa zone que possible donc effectuait des dégagements plus risqués.
                        Manchester City était plus comfortable avec la possession, donc effectuait des petites passes pour batir le jeux pour l'offensive en partant de la défense.
                    '''
                )
            ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=figGoalers,
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

create_template()

#viz1: Pressions 
data_press_viz_chel, data_press_viz_man = prep_data_press()
figPressureChel = bar_chart.draw_pressure_viz(data_press_viz_chel, 'Chelsea', True)
figPressureMan = bar_chart.draw_pressure_viz(data_press_viz_man, 'Manchester City', False)

#viz2: Touches par zone
data_poss_viz = prep_data_poss()
figPoss = bar_chart.touches_viz(data_poss_viz)

#viz3: Rendement des passes
data_pass_viz_chel, data_pass_viz_man = prep_data_pass()
figPassChel = bar_chart.passes_viz(data_pass_viz_chel, 'Chelsea')
figPassMan = bar_chart.passes_viz(data_pass_viz_man, 'Manchester City')

#viz4: Tirs au cours du match
data_shot_viz_chel, data_shot_viz_man = prep_data_shot()
figShots = bar_chart.shot_viz(data_shot_viz_chel, data_shot_viz_man)

#viz5: Rendement des passes des gardiens
data_goaler_viz_chel, data_goaler_viz_man = prep_data_goaler()
figGoalers = bar_chart.goaler_viz(data_goaler_viz_chel, data_goaler_viz_man)

app.layout = init_app_layout(figPressureChel, figPressureMan, figPoss, figPassChel, figPassMan, figShots, figGoalers)