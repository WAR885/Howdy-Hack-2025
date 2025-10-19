from playwright.sync_api import sync_playwright
import re, html
from datetime import datetime
from zoneinfo import ZoneInfo

URL = "https://12thman.com/sports/football/schedule/text "

raw_html = ''
def fetch_football_game():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
        page.goto(URL, wait_until="domcontentloaded")
        # Wait for the schedule to be inserted into the DOM
        page.wait_for_selector("#scheduleTextPage, .sidearm-schedule-event, table", timeout=30000)
        # Some sites lazy-load on scroll; ensure everything is rendered
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        container = page.wait_for_selector("#scheduleTextPage", timeout=30000)
        raw_html = container.inner_html()
        browser.close()
        data = re.split(pattern=r'(?s)<[^>]*>', string=raw_html)
        i = 0
        while i < len(data):
            if(data[i] == '' or re.match(pattern=r'[- ]+',string=data[i]) or re.match(pattern=r'[WDL] \d+\-\d+', string=data[i])):
                data.pop(i)
                i-=1
            i+=1

        data = data[data.index('Neutral')+2:]

        game_list = []
        for i in range(0, len(data), 5):
            game_list.append({"Date":data[i],"Time":data[i+1],"Location":data[i+4],"Opponent":data[i+3]})
        
        season_year = datetime.now().year

        full_months = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December",
        }
        
        for i in range(len(game_list)):
            game = game_list[i]
            if(game['Time'] == 'Flex' or game['Time'] == 'Early'):
                game['Time'] = '12:00 PM'
            date_clean = re.sub(r'\(.+\)', '', game['Date']).strip() # "Oct 25"
            short_month = re.search(r'\w{3}',date_clean).group(0)
            date_clean = date_clean.replace(short_month,full_months[short_month])
            dt = datetime.strptime(f"{date_clean} {game['Time']} {season_year}", "%B %d %I:%M %p %Y")
            dt = dt.replace(tzinfo=ZoneInfo("America/Chicago"))
            del game['Date']
            del game['Time']
            game['Datetime'] = dt
            game['Event_Type'] = 'football_game'
            game['Title'] = f'Texas A&M vs. {game['Opponent']}'
            del game['Opponent']
    return game_list




