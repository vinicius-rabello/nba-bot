import nba_scraper.constants as const  # Importa as constantes definidas no módulo nba_scraper
from selenium import webdriver  # Importa o WebDriver do Selenium para controle do navegador
from selenium.webdriver.common.by import By  # Importa o localizador de elementos
from selenium.common.exceptions import NoSuchElementException  # Para tratamento de exceções
import os  # Para manipulação de diretórios e variáveis de ambiente


class NbaScraper(webdriver.Chrome):
    """
    Classe para raspar informações sobre jogos da NBA usando Selenium.
    Herda da classe webdriver.Chrome para controlar o navegador Chrome.
    """

    def __init__(self, driver_path=r"C:\SeleniumDrivers"):
        """
        Inicializa a classe, configurando o caminho do driver do Chrome e iniciando o navegador.

        Args:
            driver_path (str): Caminho para o diretório onde está o driver do Chrome.
        """
        self.driver_path = driver_path
        
        # Evita duplicações ao adicionar o caminho do driver
        if self.driver_path not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + self.driver_path
        
        # Inicializa o WebDriver
        super(NbaScraper, self).__init__()
        
        self.implicitly_wait(5)  # Define um tempo de espera implícito de 5 segundos
        self.minimize_window()  # Minimiza a janela do navegador para melhor desempenho

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Garante que o navegador seja fechado corretamente ao sair do contexto.
        """
        print("Closing the NbaScraper...")
        self.quit()

    def land_first_page(self):
        """Acessa a página inicial da NBA definida em `const.BASE_URL`."""
        self.get(const.BASE_URL)

    def get_schedule_days(self):
        """
        Retorna todos os blocos de dias com jogos na programação.

        Returns:
            list: Lista de elementos representando os dias da programação.
        """
        return self.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleDay_sd_')]")

    def get_schedule_day_date(self, schedule_day):
        """
        Obtém a data de um dia específico da programação.

        Args:
            schedule_day (WebElement): Elemento do dia da programação.

        Returns:
            str: Data do dia da programação.
        """
        return schedule_day.find_element(By.XPATH, ".//h4[contains(@class, 'ScheduleDay_sdDay')]").get_attribute("textContent")

    def get_schedule_day_games(self, schedule_day):
        """
        Obtém o bloco de jogos de um determinado dia.

        Args:
            schedule_day (WebElement): Elemento do dia da programação.

        Returns:
            WebElement: Bloco contendo os jogos do dia.
        """
        return schedule_day.find_element(By.XPATH, ".//div[contains(@class, 'ScheduleDay_sdGames')]")

    def get_schedule_games(self, schedule_day_games):
        """
        Retorna a lista de jogos dentro de um bloco de jogos.

        Args:
            schedule_day_games (WebElement): Elemento que contém os jogos de um dia.

        Returns:
            list: Lista de elementos representando os jogos.
        """
        return schedule_day_games.find_elements(By.XPATH, "./div[contains(@class, 'ScheduleGame')]")

    def get_schedule_game_time(self, schedule_game):
        """
        Obtém o horário do jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            str: Horário do jogo ou status do evento.
        """
        schedule_status_text = schedule_game.find_element(By.XPATH, ".//span[contains(@class, 'ScheduleStatusText')]")
        return schedule_status_text.text

    def get_schedule_game_broadcaster(self, schedule_game):
        """
        Obtém o canal de transmissão do jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            str: Nome da emissora ou 'NBA League Pass' caso não esteja especificado.
        """
        try:
            return schedule_game.find_element(By.XPATH, ".//p[contains(@class, 'Broadcasters')]").text
        except NoSuchElementException:  # Captura apenas a exceção esperada
            return "NBA League Pass"

    def get_schedule_game_teams(self, schedule_game):
        """
        Obtém os nomes das equipes que disputarão o jogo.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            list: Lista contendo os nomes das equipes (mandante e visitante).
        """
        teams = schedule_game.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgTeam')]")
        return [team.find_element(By.XPATH, ".//a").text for team in teams]

    def get_schedule_game_location(self, schedule_game):
        """
        Obtém o local onde o jogo será realizado.

        Args:
            schedule_game (WebElement): Elemento representando um jogo.

        Returns:
            tuple: Nome da arena, cidade e estado onde o jogo será realizado.
        """
        location_inner = schedule_game.find_element(By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgLocationInner')]")
        location_details = location_inner.find_elements(By.XPATH, ".//div")
        
        arena = location_details[0].get_attribute("textContent")
        city_state = location_details[1].get_attribute("textContent")

        # Divide cidade e estado, garantindo a remoção de espaços desnecessários
        city, state = map(str.strip, city_state.split(","))

        return arena, city, state