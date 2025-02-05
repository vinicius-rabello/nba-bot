from datetime import datetime
import hashlib

def month_name_to_num(month_name):
    """
    Converte o nome do mês para seu número correspondente.

    Parâmetros:
        month_name (str): Nome do mês em inglês (exemplo: "January", "February").

    Retorno:
        int: Número do mês correspondente (1 a 12) ou None se não for encontrado.
    """
    MONTH_TO_NUM = {
        "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
    }

    # Converte para minúsculas para evitar erros de formatação
    return MONTH_TO_NUM.get(month_name.lower())

def format_date(input_date, timezone=None):
    """
    Formata a data extraída da página para o formato YYYY-MM-DD.

    Parâmetros:
        input_date (str): Data no formato "Day, Month DD" (exemplo: "Friday, March 15").
        timezone (datetime.tzinfo, opcional): Fuso horário para considerar o ano corretamente.

    Retorno:
        str: Data formatada no formato "YYYY-MM-DD".
    """
    # Obtém o ano atual considerando o fuso horário (se fornecido)
    today = datetime.now(tz=timezone)
    year = today.year

    try:
        # Extrai o mês e o dia da string de entrada
        date_string = input_date.split(', ')[1].strip()
        month_name, day = date_string.split(' ')
        day = int(day.strip())

        # Converte o nome do mês para número
        month = month_name_to_num(month_name)
        if month is None:
            raise ValueError(f"Nome do mês inválido: {month_name}")

        # Se o mês for janeiro e estivermos em dezembro, o ano deve ser ajustado para o próximo
        if month < today.month:
            year += 1

        # Retorna a data formatada no padrão ISO (YYYY-MM-DD)
        return f"{year:04d}-{month:02d}-{day:02d}"

    except (IndexError, ValueError) as e:
        raise ValueError(f"Erro ao processar data '{input_date}': {e}")

def generate_game_id(date, home_team, away_team):
    """
    Gera um ID único para cada jogo baseado na data e nos times.

    Parâmetros:
        date (str): Data do jogo no formato 'YYYY-MM-DD'.
        home_team (str): Nome do time da casa.
        away_team (str): Nome do time visitante.

    Retorno:
        str: ID único gerado como hash SHA-1.
    """
    raw_id = f"{date}_{home_team}_{away_team}".lower().replace(" ", "_")
    return hashlib.sha1(raw_id.encode()).hexdigest()[:10]  # Hash curto para evitar IDs longos