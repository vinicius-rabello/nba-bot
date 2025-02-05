# Importa a classe NbaScraper para raspagem de dados
from nba_scraper.nba_scraper import NbaScraper  
# Importa a função para formatar datas
from nba_scraper.utils import format_date  
import pandas as pd  # Para manipulação de dados
from tqdm import tqdm  # Para exibição de progresso
from zoneinfo import ZoneInfo # Para formatação das datas

import nba_scraper.constants as const  # Importa as constantes definidas no módulo nba_scraper

def scrape_nba_task():
    # Define a zona de fuso horário para a formatação das datas
    tz = ZoneInfo(const.TIMEZONE)

    # Lista para armazenar os dados raspados
    data = []

    # Inicia o Web Scraper dentro de um gerenciador de contexto para garantir que o WebDriver seja fechado corretamente
    with NbaScraper() as scraper:
        scraper.land_first_page()  # Acessa a página principal da NBA
        
        # Obtém a lista de dias disponíveis na programação
        schedule_days = scraper.get_schedule_days()
        
        # Itera sobre os dias da programação (atualmente pegando apenas a primeiro semana [:7])
        for schedule_day in tqdm(schedule_days[:7], desc="Processando dias"):
            schedule_day_games = scraper.get_schedule_day_games(schedule_day)  # Obtém os jogos do dia
            schedule_games = scraper.get_schedule_games(schedule_day_games)  # Obtém a lista de jogos
            full_date = format_date(scraper.get_schedule_day_date(schedule_day), timezone=tz)  # Obtém e formata a data do dia
            
            # Itera sobre os jogos do dia
            for schedule_game in tqdm(schedule_games, desc="Processando jogos", leave=False):
                # Coleta as informações do jogo
                game_time = scraper.get_schedule_game_time(schedule_game)
                broadcaster = scraper.get_schedule_game_broadcaster(schedule_game)
                away_team, home_team = scraper.get_schedule_game_teams(schedule_game)
                arena, city, state = scraper.get_schedule_game_location(schedule_game)
                
                # Adiciona os dados do jogo à lista
                data.append([full_date, game_time, broadcaster, home_team, away_team, arena, city, state])

    # Converte os dados coletados para um DataFrame do pandas
    df = pd.DataFrame(data, columns=['date', 'time', 'broadcaster', 'home_team', 'away_team', 'arena', 'city', 'state'])

    return df