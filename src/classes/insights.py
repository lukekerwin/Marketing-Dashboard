import pandas as pd

from classes.sdn import sdn

class Insights:
    def __init__(self):
        pass    

    def gain_insights(self, bets):
        df = pd.DataFrame(bets)   
        df['ID'] = df['id'].astype(int)
        df['Date'] = df['date']
        df['Capper'] = df['capper'].apply(lambda x: x['name'])
        df['Pick'] = df['pick']
        df['League'] = df['league_id'].apply(lambda x: [item['abbreviation'].upper() for item in sdn.leagues if item['id'] == x][0] if x else None)
        df['Team'] = df['team'].apply(lambda x: str(x['location_name'])+' '+str(x['team_name']) if x else None)
        df['Bet Type'] = df['bet_type'].apply(lambda x: x['name'] if x else None)
        df['Bet Subtype'] = df['bet_subtype'].apply(lambda x: x['name'] if x else None)
        df['Bet Prop'] = df['bet_prop'].apply(lambda x: x['name'] if x else None)
        df['Bet Length'] = df['bet_length'].apply(lambda x: x['name'] if x else None)
        df['Line'] = df['line']
        df['Odds'] = df['odds']
        df['Unit'] = df['unit']
        df['Result'] = df['result']
        df['Is Parlay'] = df['parlay_id'].apply(lambda x: True if x else False)
        df['Is Premium'] = df['is_premium'].apply(lambda x: True if x==1 else False)
        df['Is Projection'] = df['is_projection'].apply(lambda x: True if x==1 else False)
        df['Is Verified'] = df['is_verified'].apply(lambda x: True if x==1 else False)
        df['Is Live'] = df['is_live'].apply(lambda x: True if x==1 else False)
        df['Sportsbook'] = df['sportsbook'].apply(lambda x: x['name'] if x else None)
        df['Player'] = df['player'].apply(lambda x: x['player_info']['first_name']+' '+x['player_info']['last_name'] if x else None)
        df = df[['ID', 'Date', 'Capper', 'Pick', 'League', 'Team', 'Bet Type', 'Bet Subtype', 'Bet Prop', 'Bet Length', 'Line', 'Odds', 'Unit', 'Result', 'Is Parlay', 'Is Premium', 'Is Projection', 'Is Verified', 'Is Live', 'Sportsbook', 'Player']]
        
        # Get Results
        results_df = pd.DataFrame(columns=['Capper', 'H', 'M', 'P'])
        df2 = df.copy()
        df2 = df2.groupby(['Capper', 'Result']).size().unstack(fill_value=0)
        if len(df2) > 0:
            df['decimal_odds'] = df['Odds'].apply(lambda x: (x/100)+1 if x > 0 else (100/abs(x))+1 if x < 0 else 0)
            df['Net Units'] = df.apply(lambda x: -1*x['Unit'] if x['Result'] == 'M' else x['Unit']*(x['decimal_odds']-1) if x['Result'] == 'H' else 0, axis=1)
            df2['Net Units'] = df.groupby('Capper')['Net Units'].sum()
            df2['Net Units Placed'] = df.groupby('Capper')['Unit'].sum()
            df2 = df2.reset_index()
            df2['Total'] = df2['H'] + df2['M'] + df2['P']
            df2['Win %'] = df2['H'] / df2['Total']
            df2['Loss %'] = df2['M'] / df2['Total']
            df2['Push %'] = df2['P'] / df2['Total']
            df2['ROI'] = df2['Net Units'] / df2['Net Units Placed']
            df2 = df2[['Capper', 'H', 'M', 'P', 'Total', 'Win %', 'Loss %', 'Push %', 'Net Units', 'Net Units Placed', 'ROI']]
        else:
            df2 = pd.DataFrame(columns=['Capper', 'H', 'M', 'P', 'Total', 'Win %', 'Loss %', 'Push %', 'Net Units', 'Net Units Placed', 'ROI'])

        return df, df2
