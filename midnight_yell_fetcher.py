from datetime import datetime
from zoneinfo import ZoneInfo

def midnight_yell_fetcher(football_games:list):
    midnight_yell_list = []
    for i in range(len(football_games)):
        game = football_games[i]
        if(game['Location'] == 'Bryan-College Station (Kyle Field)'):
            dt = game['Datetime'].replace(hour=0, minute=0, second=0, microsecond=0)
            yell_info = {"Datetime":dt, "Location": "Bryan-College Station (Kyle Field)", 
                         'Title': f'{game['Title']} Midnight Yell', 'Event_Type': 'midnight_yell'}
            midnight_yell_list.append(yell_info)
    return(midnight_yell_list)