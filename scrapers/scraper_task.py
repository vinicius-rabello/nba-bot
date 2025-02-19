# Importa a classe NbaScraper para raspagem de dados
from nba_scraper.nba_scraper import NbaScraper  
# Importa a função para formatar datas
from nba_scraper.utils import format_date, generate_game_id, get_month_from_date_string, month_num_to_name
# Import a função que valida os dados
from validation.validate_game import validate_game
import pandas as pd  # Para manipulação de dados
from tqdm import tqdm  # Para exibição de progresso
from zoneinfo import ZoneInfo # Para formatação das datas

import nba_scraper.constants as const  # Importa as constantes definidas no módulo nba_scraper

def scrape_nba_task(date_str):
    # Pega o mês da data requisitada
    month_num = get_month_from_date_string(date_str)
    month_name = month_num_to_name(month_num)
    url = const.BASE_URL
    url = url.replace("MONTH", month_name)

    # Define a zona de fuso horário para a formatação das datas
    tz = ZoneInfo(const.TIMEZONE)

    # Lista para armazenar os dados raspados
    data = []

    # Inicia o Web Scraper dentro de um gerenciador de contexto para garantir que o WebDriver seja fechado corretamente
    with NbaScraper() as scraper:
        scraper.land_first_page(url=url)  # Acessa a página principal da NBA
        # Obtém a lista de dias disponíveis na programação
        schedule_days = scraper.get_schedule_days()
        
        # no caso de existirem menos de 7 elementos de dia na página, pegue a quantidade restante
        # Itera sobre os dias da programação (atualmente pegando apenas a primeiro semana [:n_days])
        for schedule_day in tqdm(schedule_days, desc=f"Procurando o dia: {date_str}"):
            full_date = format_date(scraper.get_schedule_day_date(schedule_day), timezone=tz)  # Obtém e formata a data do dia
            # Se a data do jogo não for a pedida pela task, pule
            if full_date != date_str:
                continue

            print(f"Jogos do dia: {date_str} encontrados")
            schedule_day_games = scraper.get_schedule_day_games(schedule_day)  # Obtém os jogos do dia
            schedule_games = scraper.get_schedule_games(schedule_day_games)  # Obtém a lista de jogos
            
            # Itera sobre os jogos do dia
            for schedule_game in tqdm(schedule_games, desc=f"Processando jogos do dia: {date_str}", leave=False):
                # Coleta as informações do jogo
                game_time = scraper.get_schedule_game_time(schedule_game)
                broadcaster = scraper.get_schedule_game_broadcaster(schedule_game)
                away_team, home_team = scraper.get_schedule_game_teams(schedule_game)
                arena, city, state = scraper.get_schedule_game_location(schedule_game)

                # Cria um Id único para a partida, baseado na data e nome dos times
                game_id = generate_game_id(full_date, home_team, away_team)

                # Cria um dicionário com os dados do jogo
                game_data = {
                    "game_id": game_id,
                    "full_date": full_date,
                    "game_time": game_time,
                    "broadcaster": broadcaster,
                    "home_team": home_team,
                    "away_team": away_team,
                    "arena": arena,
                    "city": city,
                    "state": state
                }

                # Valida os dados do jogo com o modelo Game do pydantic
                validated_game = validate_game(game_data)
                if validated_game:
                    # Adiciona os dados do jogo à lista se forem válidos
                    data.append([validated_game.game_id, validated_game.full_date, validated_game.game_time,
                                 validated_game.broadcaster, validated_game.home_team, validated_game.away_team,
                                 validated_game.arena, validated_game.city, validated_game.state])
                else:
                    print(f"Dados inválidos para o jogo: {game_data}")
            
            # Converte os dados coletados para um DataFrame do pandas
            df = pd.DataFrame(data, columns=['game_id', 'date', 'time', 'broadcaster', 'home_team', 'away_team', 'arena', 'city', 'state'])
            return df

df = scrape_nba_task('2025-01-02')
if df is not None:
    df.to_excel('test.xlsx', index=False)
else:
    print('No games found')