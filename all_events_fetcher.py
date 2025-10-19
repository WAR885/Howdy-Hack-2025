from datetime import datetime
from zoneinfo import ZoneInfo
from midnight_yell_fetcher import *
from football_games_fetcher import *
import zoneinfo

def fetch_all_events():
    current_year = datetime.now().year
    muster = {'Datetime':datetime(year=current_year,month=4,day=21,hour=17,minute=0,
                            second=0,microsecond=0),'Location':'Reed Arena', 'Title': 'Muster',
                            'Event_Type': 'muster'}
    football_games = fetch_football_game()
    elephant_walk = {'Datetime':football_games[len(football_games)-1]['Datetime'].replace(hour=18,minute=0,second=0),'Location':'Reed Arena'
                    , 'Title': 'Elephant Walk', 'Event_Type': 'elephant_walk'}
    midnight_yell_games = midnight_yell_fetcher(football_games)

    total_events = football_games
    total_events += midnight_yell_games
    total_events += [muster,elephant_walk]
    for i in range(len(total_events)):
        chicago_time = datetime.now(ZoneInfo("America/Chicago"))
        total_events[i]['Datetime'] = total_events[i]['Datetime'].replace(tzinfo=ZoneInfo("America/Chicago"))
        if total_events[i]['Datetime'] > chicago_time:
            total_events[i]['has_passed'] = False
        else:
            total_events[i]['has_passed'] = True
    return total_events