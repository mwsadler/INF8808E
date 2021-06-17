'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from pandas.core.frame import DataFrame
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # DONE : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act

    dfTotal = my_df.groupby(['Act']).count().drop(['Scene', 'PlayerLine'], axis=1)
    dfCount = my_df.groupby(['Act', 'Player']).count().drop(['Scene', 'PlayerLine'], axis=1)

    dfCount['LinePercentage'] = round((dfCount.Line / dfTotal.Line) * 100, 2)
    dfCount = dfCount.rename(columns={'Line':'LineCount'})

    return dfCount


def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other plyaers
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # DONE : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage
    df = my_df.copy(deep=True).reset_index()
    
    dfSum = my_df.copy(deep=True)
    dfSum = dfSum.groupby(['Player']).sum()
    
    players = dfSum['LineCount'].nlargest(5).reset_index()
    players = players.drop(['LineCount'], axis=1)
    
    romeo = df[df['Player'] == players.Player[0]]
    juliet = df[df['Player'] == players.Player[1]]
    nurse = df[df['Player'] == players.Player[2]]
    benvolio = df[df['Player'] == players.Player[3]]
    mercutio = df[df['Player'] == players.Player[4]]
    dfTop = pd.concat([romeo,juliet, nurse, benvolio, mercutio])
    


    # allPlayer = groupby(['player']).drop(tout sauf player)
    # smallestPlayers = (merge allPlayer avec players).drop_duplicate)
    # higherplayer = my_df.merge(smallestPlayers).drop_duplicate()

    # dfTop = my_df.copy(deep=True)
   
    
    # dfTop['LineCount'] = my_df['LineCount'].nlargest(5)
    # dfTop = dfTop.dropna().reset_index()
    # print(dfTop)
    
    dfBot = pd.concat([dfTop, df]).drop_duplicates(keep=False) # difference
    dfBot = dfBot.groupby(['Act']).sum().reset_index()
    
    dfBot.insert(0, 'Player', 'Others')
    # Replace par Act to create others row
    df = pd.concat([dfBot,dfTop])
    # print(df.sort_values(['Act', 'LineCount'], ascending = True))
    # print(dfTop.loc[dfTop['Act'].isin([1])]) 


    return df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # DONE : Clean the player names
    dfClean = my_df.copy(deep=True)
    dfClean['Player'] = my_df['Player'].str.title()

    return dfClean

def clean_pressure(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
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
    print(df)
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
    return my_df

def clean_goaler(my_df):
    my_df = clean_pass(my_df)
    my_df = my_df.loc[[13]].reset_index()
    my_df['CourtReussis'] = my_df.apply(lambda x: x['CourtReussis'] + x['MoyenReussis'], axis=1)
    my_df['CourtRate'] = my_df.apply(lambda x: x['CourtRate'] + x['MoyenRate'], axis=1)
    my_df['TotalCourt'] = my_df.apply(lambda x: x['CourtRate'] + x['CourtReussis'], axis=1)
    my_df['TotalLong'] = my_df.apply(lambda x: x['LongRate'] + x['LongReussis'], axis=1)
    my_df = my_df.drop(['index', 'MoyenReussis', 'MoyenRate'], axis=1)

    return my_df

