from datetime import datetime
from zoneinfo import ZoneInfo
from midnight_yell_fetcher import *
from football_games_fetcher import *

muster = {'date':datetime(year=datetime.now().year,month=4,day=21,hour=17,minute=0,
                          second=0,microsecond=0),'Location':'Reed Arena'}
football_games = fetch_football_game()
elephant_walk = {'date':football_games[len(football_games)-1]['Datetime'].replace(hour=18,minute=0,second=0),'Location':'Reed Arena'}
midnight_yell_games = midnight_yell_fetcher(football_games)