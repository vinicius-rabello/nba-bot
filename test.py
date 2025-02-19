from tasks import insert_task
import pandas as pd

df = pd.read_excel('test.xlsx')
insert_task.insert_nba_games(df)