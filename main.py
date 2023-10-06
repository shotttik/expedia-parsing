from Core.webdriver import Browser
from Core.config import config_browser, get_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Handlers.flight_data_handler import FlightDataHandler
from Pages.home_page import HomePage
import time

from Pages.search_page import SearchPage

if '__main__' == __name__:
    '''Configuring browser'''
    config_browser_data = config_browser()
    browser_i = Browser(config_browser_data)
    data = get_data()
    Browser.driver.get(data['start_url'])
    '''Home Page'''
    home_page = HomePage(browser_i.wait_time)
    home_page.verify_page()
    # loading excel to dataframe
    flight_data_handler = FlightDataHandler(data["flights_file"])
    flight_df = flight_data_handler.pending_flight_row
    home_page.configure_search_controls(flight_df)
    Browser.save_screenshot()
    home_page.go_to_search_page()
    # when clicking search opens a new window
    Browser.change_window_by_id(1)
    '''Search Page'''
    search_page = SearchPage(browser_i.wait_time)
    search_page.verify_page()
    # search_page.check_direct_flight(flight_df["Direct Flight"])
    # SCRAPE LOGIC
    # @TODO
    # # SCRAPE LOGIC
    # flight_data_handler.update_specific_row(flight_df)
    # while True:
    #     flight_df = flight_data_handler.pending_flight_row
    #     if not flight_df:
    #         break
    #     # DO LOGIC AFTER ONE ROW ON SEARCH PAGE
    #     search_page.update_search_controls(flight_df)
    #     # DO LOGIC AFTER ONE ROW  ON SERACH PAGE
    Browser.save_screenshot("screenshot1.png")
    Browser.quit()
    # main_page.go_to_parsing_page()
