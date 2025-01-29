import nba_scraper.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
import os


class NbaScraper(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers"):
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        super(NbaScraper, self).__init__()
        self.implicitly_wait(5)
        self.minimize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the NbaScraper...")
        self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def get_schedule_days(self):
        schedule_days = self.find_elements(By.XPATH, ".//div[contains(@class, 'ScheduleDay_sd_')]")
        return schedule_days
    
    def get_schedule_day_date(self, schedule_day):
        schedule_day_date = schedule_day.find_element(By.XPATH, ".//h4[contains(@class, 'ScheduleDay_sdDay')]").get_attribute("textContent")
        return schedule_day_date


    def get_schedule_day_games(self, schedule_day):
        schedule_day_games = schedule_day.find_element(
            By.XPATH, ".//div[contains(@class, 'ScheduleDay_sdGames')]")
        return schedule_day_games

    def get_schedule_games(self, schedule_day_games):
        schedule_games = schedule_day_games.find_elements(
                By.XPATH, "./div[contains(@class, 'ScheduleGame')]")
        return schedule_games

    def get_schedule_game_time(self, schedule_game):
        schedule_status_text = schedule_game.find_element(
            By.XPATH, ".//span[contains(@class, 'ScheduleStatusText')]")
        schedule_game_time = schedule_status_text.text
        return schedule_game_time

    def get_schedule_game_broadcaster(self, schedule_game):
        try:
            schedule_game_broadcasters = schedule_game.find_element(
                By.XPATH, ".//p[contains(@class, 'Broadcasters')]").text
        except:
            schedule_game_broadcasters = 'NBA League Pass'
        return schedule_game_broadcasters

    def get_schedule_game_teams(self, schedule_game):
        schedule_game_teams = schedule_game.find_elements(
            By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgTeam')]")
        sg_team_names = [sg_team.find_element(
            By.XPATH, ".//a").text for sg_team in schedule_game_teams]
        return sg_team_names

    def get_schedule_game_location(self, schedule_game):
        schedule_game_location_inner = schedule_game.find_element(
            By.XPATH, ".//div[contains(@class, 'ScheduleGame_sgLocationInner')]")
        schedule_game_location_inner_divs = schedule_game_location_inner.find_elements(
            By.XPATH,".//div")
        arena = schedule_game_location_inner_divs[0].get_attribute("textContent")
        city_state = schedule_game_location_inner_divs[1].get_attribute("textContent")
        city, state = city_state.split(',')
        state = state.strip()
        return arena, city, state