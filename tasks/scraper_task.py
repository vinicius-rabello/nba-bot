def scrape_nba_task(date_str):
    import sys
    from pathlib import Path

    root_dir = Path(__file__).resolve().parent.parent
    sys.path.append(str(root_dir))
    sys.path.append("/opt/airflow/scrapers")

    from scrapers.nba_scraper.nba_scraper import NbaScraper
    from scrapers.nba_scraper.utils import format_date, generate_game_id, get_month_from_date_string, month_num_to_name
    from scrapers.validation.validate_game import validate_game
    import pandas as pd
    from tqdm import tqdm
    from zoneinfo import ZoneInfo
    import time

    import scrapers.nba_scraper.constants as const
    
    month_num = get_month_from_date_string(date_str)
    month_name = month_num_to_name(month_num)
    url = const.BASE_URL.replace("MONTH", month_name)
    
    print(f"URL being accessed: {url}")  # Debug log
    
    tz = ZoneInfo(const.TIMEZONE)
    data = []
    games_found = False

    try:
        with NbaScraper() as scraper:
            print("Iniciando o scraper...")  # Debug log
            scraper.land_first_page(url=url)
            print("Página inicial acessada com sucesso")  # Debug log
            
            # Adicionando espera de 5 segundos antes de pegar os dias
            print("Aguardando 5 segundos para carregar o conteúdo...")
            time.sleep(5)
            schedule_days = scraper.get_schedule_days()
            print(schedule_days)
            print(f"Dias encontrados na programação: {len(schedule_days)}")  # Debug log
            
            if not schedule_days:
                print("Nenhum dia encontrado na programação!")
                return pd.DataFrame()

            for schedule_day in tqdm(schedule_days, desc=f"Procurando o dia: {date_str}"):
                try:
                    print("Processando dia da programação...")  # Debug log
                    full_date = format_date(scraper.get_schedule_day_date(schedule_day), timezone=tz)
                    print(f"Data formatada: {full_date}")  # Debug log
                    
                    if full_date != date_str:
                        print(f"Data não corresponde: {full_date} != {date_str}")  # Debug log
                        continue

                    games_found = True
                    print(f"Jogos do dia: {date_str} encontrados")
                    schedule_day_games = scraper.get_schedule_day_games(schedule_day)
                    schedule_games = scraper.get_schedule_games(schedule_day_games)
                    
                    print(f"Número de jogos encontrados: {len(schedule_games)}")  # Debug log

                    for schedule_game in tqdm(schedule_games, desc=f"Processando jogos do dia: {date_str}", leave=False):
                        try:
                            print("Processando jogo individual...")  # Debug log
                            game_time = scraper.get_schedule_game_time(schedule_game)
                            broadcaster = scraper.get_schedule_game_broadcaster(schedule_game)
                            away_team, home_team = scraper.get_schedule_game_teams(schedule_game)
                            away_team_score, home_team_score = scraper.get_schedule_game_scores(schedule_game)
                            arena, city, state = scraper.get_schedule_game_location(schedule_game)

                            print(f"Dados coletados para: {away_team} @ {home_team}")  # Debug log

                            game_id = generate_game_id(full_date, home_team, away_team)
                            game_data = {
                                "game_id": game_id,
                                "full_date": full_date,
                                "game_time": game_time,
                                "broadcaster": broadcaster,
                                "home_team": home_team,
                                "away_team": away_team,
                                "home_team_score": home_team_score,
                                "away_team_score": away_team_score,
                                "arena": arena,
                                "city": city,
                                "state": state
                            }

                            validated_game = validate_game(game_data)
                            if validated_game:
                                data.append([
                                    validated_game.game_id, validated_game.full_date,
                                    validated_game.game_time, validated_game.broadcaster,
                                    validated_game.home_team, validated_game.away_team,
                                    validated_game.home_team_score, validated_game.away_team_score,
                                    validated_game.arena, validated_game.city, validated_game.state
                                ])
                                print(f"Jogo adicionado com sucesso: {game_id}")  # Debug log
                            else:
                                print(f"Dados inválidos para o jogo: {game_data}")
                        except Exception as e:
                            print(f"Erro ao processar jogo individual: {str(e)}")
                            continue
                except Exception as e:
                    print(f"Erro ao processar dia: {str(e)}")
                    continue

        if not games_found:
            print(f"Nenhum jogo encontrado para a data: {date_str}")
            return pd.DataFrame()

        if not data:
            print(f"Nenhum dado válido encontrado para a data: {date_str}")
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            'game_id', 'date', 'time', 'broadcaster', 'home_team', 'away_team',
            'home_team_score', 'away_team_score', 'arena', 'city', 'state'
        ])
        
        print(f"DataFrame final shape: {df.shape}")
        return df

    except Exception as e:
        print(f"Erro durante a execução do scraper: {str(e)}")
        raise