'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from pandas.core.frame import DataFrame
from modes import MODE_TO_COLUMN

def clean_pressure(my_df):
    my_df.rename( columns={'Unnamed: 0':'Joueur', 'Pressions':'PressionsRate', 'Pressions.1':'PressionsReussis'}, inplace=True )
    my_df = my_df[['Joueur', 'PressionsRate', 'PressionsReussis']]
    my_df = my_df.drop([0, 15]).reset_index()
    my_df = my_df.drop(['index'], axis=1)
    my_df[['PressionsReussis', 'PressionsRate']] = my_df[['PressionsReussis', 'PressionsRate']].apply(pd.to_numeric)
    my_df.sort_values(['PressionsRate'], ascending=False, inplace=True)
    my_df['PressionsRate'] = my_df.apply(lambda x: x['PressionsRate'] - x['PressionsReussis'], axis=1)
    my_df['Joueur'] = my_df.apply(lambda x: x['Joueur'][0: x['Joueur'].index('\\')], axis=1)
    return my_df

def clean_pass(my_df):
    my_df.rename( columns={'Unnamed: 0':'Joueur', 'Court':'CourtReussis', 'Court.1':'CourtRate', 'Moyen':'MoyenReussis', 'Moyen.1':'MoyenRate', 'Long':'LongReussis', 'Long.1':'LongRate', 'Total.1': 'TotalPasse'}, inplace=True )
    my_df = my_df[['Joueur','TotalPasse', 'CourtReussis', 'CourtRate', 'MoyenReussis', 'MoyenRate', 'LongReussis', 'LongRate']]
    my_df = my_df.drop([0, 15]).reset_index()
    my_df = my_df.drop(['index'], axis=1)
    my_df[['TotalPasse', 'CourtReussis', 'CourtRate', 'MoyenReussis', 'MoyenRate', 'LongReussis', 'LongRate']] = my_df[['TotalPasse', 'CourtReussis', 'CourtRate', 'MoyenReussis', 'MoyenRate', 'LongReussis', 'LongRate']].apply(pd.to_numeric)    
    my_df['Joueur'] = my_df.apply(lambda x: x['Joueur'][0: x['Joueur'].index('\\')], axis=1)
    my_df['CourtRate'] = my_df.apply(lambda x: x['CourtRate'] - x['CourtReussis'], axis=1)
    my_df['MoyenRate'] = my_df.apply(lambda x: x['MoyenRate'] - x['MoyenReussis'], axis=1)
    my_df['LongRate'] = my_df.apply(lambda x: x['LongRate'] - x['LongReussis'], axis=1)
    my_df.sort_values(['TotalPasse'], ascending=False, inplace=True)
    return my_df


def clean_poss(my_df1, my_df2):
    my_df1.rename( columns={'Touches.2':'ZoneDefensive', 'Touches.3':'ZoneMilieu', 'Touches.4':'ZoneAttaque' }, inplace=True )
    my_df1 = my_df1[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']]
    my_df2.rename( columns={'Touches.2':'ZoneDefensive', 'Touches.3':'ZoneMilieu', 'Touches.4':'ZoneAttaque' }, inplace=True )
    my_df2 = my_df2[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']]
    my_df1 = my_df1.drop([0, 15]).reset_index()
    my_df2 = my_df2.drop([0, 15]).reset_index()
    my_df1[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']] = my_df1[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']].apply(pd.to_numeric)    
    my_df2[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']] = my_df2[['ZoneDefensive', 'ZoneMilieu', 'ZoneAttaque']].apply(pd.to_numeric)    
    d = {'Zone': ['Zone défensive', 'Zone centrale', 'Zone offensive'] ,'Chelsea': [my_df1["ZoneDefensive"].sum(), my_df1["ZoneMilieu"].sum(), my_df1["ZoneAttaque"].sum()], 'Man city': [my_df2["ZoneDefensive"].sum(), my_df2["ZoneMilieu"].sum(), my_df2["ZoneAttaque"].sum()]}
    df = pd.DataFrame(data=d)
    return df

def clean_shot(my_df):
    my_df.rename( columns={'Unnamed: 0':'Minute', 'Unnamed: 2':'Equipe', 'Unnamed: 3':'Resultat', 'Unnamed: 4':'Distance' }, inplace=True )
    my_df = my_df[['Minute', 'Equipe', 'Resultat', 'Distance']]
    my_df = my_df.drop([0, 9]).reset_index()
    my_df = my_df.drop(['index'], axis=1)
    my_df['Equipe'] = my_df.apply(lambda x: 'Man' if x['Equipe'] == 'Manchester City' else 'Che', axis=1)
    my_df['Resultat'] = my_df.apply(lambda x: 'C' if x['Resultat'] == 'Sauvée' or  x['Resultat'] == 'Bloquée' else x['Resultat'], axis=1)
    my_df['Resultat'] = my_df.apply(lambda x: 'NC' if x['Resultat'] == 'Non cadrée' else x['Resultat'], axis=1)
    my_df['Minute'] = my_df.apply(lambda x: sum(int(i) for i in x['Minute'].split('+')), axis=1)
    my_df[['Distance', 'Minute']] = my_df[['Distance', 'Minute']].apply(pd.to_numeric)

    df_man = my_df
    df_man = df_man.loc[df_man['Equipe'] == 'Man']
    df_chel = my_df
    df_chel = df_chel.loc[df_chel['Equipe'] == 'Che']
    df_chel = df_chel.drop(['Equipe'], axis=1).reset_index()
    df_chel = df_chel.drop(['index'], axis=1)
    df_man = df_man.drop(['Equipe'], axis=1).reset_index()
    df_man = df_man.drop(['index'], axis=1)

    return df_chel, df_man

def clean_goaler(my_df):
    my_df = clean_pass(my_df)
    my_df = my_df.loc[[13]].reset_index()
    my_df['CourtReussis'] = my_df.apply(lambda x: x['CourtReussis'] + x['MoyenReussis'], axis=1)
    my_df['CourtRate'] = my_df.apply(lambda x: x['CourtRate'] + x['MoyenRate'], axis=1)
    my_df['TotalCourt'] = my_df.apply(lambda x: x['CourtRate'] + x['CourtReussis'], axis=1)
    my_df['TotalLong'] = my_df.apply(lambda x: x['LongRate'] + x['LongReussis'], axis=1)
    my_df = my_df.drop(['index', 'MoyenReussis', 'MoyenRate', 'TotalPasse'], axis=1)

    print(my_df)
    return my_df
