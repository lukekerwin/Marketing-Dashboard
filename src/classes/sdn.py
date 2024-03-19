import requests
from datetime import datetime, timedelta
import pandas as pd

class SDN:
    def __init__(self):
        self.base_url = 'https://f3tz8x1ut5.execute-api.us-east-2.amazonaws.com/'
        self.session = requests.Session()
        self.bets = {}
        self.leagues = self.session.get(self.base_url + 'league').json()
        self.bet_types = self.session.get(self.base_url + 'bet/type').json()
        self.subtypes = self.session.get(self.base_url + 'bet/subtype').json()
        self.props = self.session.get(self.base_url + 'bet/prop').json()
        self.lengths = self.session.get(self.base_url + 'bet/length').json()
        self.sportsbooks = self.session.get(self.base_url + 'bet/sportsbook').json()

    def filter_format(self, data, type=None):
        if type == 'league':
            return [item['abbreviation'].upper()+' - '+item['name'] for item in data]
        else:
            return sorted([item['name'] for item in data])
        
    def get_bets(self, start_date:str, end_date:str):
        date_range = pd.date_range(start=start_date, end=end_date)
        output = []
        for date in date_range:
            date = date.strftime('%Y-%m-%d')
            if date in self.bets:
                output.extend(self.bets[date])
            else:
                bets = self.__get_bets(date)
                self.bets[date] = bets
                output.extend(bets)
        return output
    
    def __get_bets(self, date:str):
        date_m_2 = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=2)).strftime('%Y-%m-%d')
        date_p_2 = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d')
        bets = self.session.get(self.base_url + f'bet?from={date_m_2}&to_date={date_p_2}&limit=1000').json()
        actual_bets = []
        for bet in bets:
            if bet['date'] == date:
                actual_bets.append(bet)
        return actual_bets
            
    
sdn = SDN()