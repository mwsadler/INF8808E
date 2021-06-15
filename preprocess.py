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
