from nba_scraper.nba_scraper import NbaScraper
import pandas as pd
from tqdm import tqdm

data = []
with NbaScraper() as scraper:
    scraper.land_first_page()
    schedule_days = scraper.get_schedule_days()
    for schedule_day in tqdm(schedule_days[:7]):
        schedule_day_games = scraper.get_schedule_day_games(schedule_day)
        schedule_games = scraper.get_schedule_games(schedule_day_games)
        date = scraper.get_schedule_day_date(schedule_day)
        for schedule_game in tqdm(schedule_games):
            time = scraper.get_schedule_game_time(schedule_game)
            broadcaster = scraper.get_schedule_game_broadcaster(schedule_game)
            away_team, home_team = scraper.get_schedule_game_teams(schedule_game)
            arena, city, state = scraper.get_schedule_game_location(schedule_game)
            data.append([date, time, broadcaster, home_team, away_team, arena, city, state])

df = pd.DataFrame(data=data, columns=['date', 'time', 'broadcaster', 'home_team', 'away_team', 'arena', 'city', 'state'])
df.to_excel('test.xlsx', index=False)