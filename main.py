import sys
from Core.webdriver import Browser
from Core.config import config_browser, get_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Exceptions.DataExceptions import FlightDataException
from Handlers.flight_data_handler import FlightDataHandler
from Pages.home_page import HomePage
from Pages.search_page import SearchPage
import time
from enums.StatusEnums import Completed

from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)

if '__main__' == __name__:
    '''Configuring browser'''
    config_browser_data = config_browser()
    browser_i = Browser(config_browser_data)
    data = get_data()
    flight_data_handler = FlightDataHandler(data["flights_file"])
    first_flight_scraping = True
    s = 0
    while True:
        try:
            flight_df = flight_data_handler.pending_flight_row
            if flight_df.empty:
                LOGGER.info("No pending flights found. Exiting...")
                Browser.quit()
                sys.exit()
            if first_flight_scraping:
                Browser.driver.get(data['start_url'])
                '''Home Page'''
                home_page = HomePage(browser_i.wait_time)
                home_page.verify_page()
                # loading excel to dataframe
                home_page.configure_search_controls(flight_df)
                Browser.save_screenshot()
                home_page.go_to_search_page()
                Browser.close_current_window()
                # when clicking search opens a new window
                Browser.change_window_by_id(0)
                '''Search Page'''
                search_page = SearchPage(browser_i.wait_time)
                search_page.handle_if_flight_not_found()
                search_page.verify_page()
                search_page.choose_cheapest_flights()
                search_page.handle_outbound(flight_df["Outbound"])
                first_flight_scraping = False
                Browser.save_screenshot(f"screenshot{s}.png")
                s += 1
            else:
                search_page.configure_search_controls(flight_df)
                Browser.save_screenshot(f"screenshot{s}.png")
                s += 1
            # SCRAPE LOGIC
            # @TODO
            # # SCRAPE LOGIC
            LOGGER.info(
                f"Row Name[{flight_df.name}] successfully scraped and updated.")
            flight_df["Completed"] = Completed.YES.value
            flight_data_handler.update_specific_row(flight_df)
        except FlightDataException as e:
            LOGGER.error(f"Row Name[{flight_df.name}]: {str(e)} ")
            flight_df["Completed"] = Completed.ERROR.value
            flight_data_handler.update_specific_row(flight_df)
        # except Exception:
        #     LOGGER.error("Got unexpected error. Please contact support")
        #     Browser.quit()
        #     sys.exit()
