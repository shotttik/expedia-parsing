import sys

import pandas as pd
from Core.webdriver import Browser
from Core.config import config_browser, get_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Exceptions.DataExceptions import FlightDataException
from Exceptions.ScrapingExceptions import ScrapingDataException
from Handlers.flight_data_handler import FlightDataHandler
from Handlers.scrape_handler import ScrapeDataHandler
from Pages.home_page import HomePage
from Pages.search_page import SearchPage
import time
from enums.StatusEnums import Status

from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)

if '__main__' == __name__:
    '''Configuring browser'''
    config_browser_data = config_browser()
    browser_i = Browser(config_browser_data)
    data = get_data()
    flight_data_handler = FlightDataHandler(data["flights_file"])
    first_flight_scraping = True
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
                home_page.accept_cookies()
                # loading excel to dataframe
                home_page.configure_search_controls(flight_df)
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
            else:
                search_page.configure_search_controls(flight_df)

            ''' SCRAPING '''
            scraper = ScrapeDataHandler()
            html_source = search_page.fetch_cheapest_item_source()
            scraper.parse_html(html_source)
            scraped_data = scraper.get_data()
            flight_df.update(pd.Series(scraped_data))
            ''' SUCCESS '''
            LOGGER.info(
                f"Row Name[{flight_df.name}] successfully scraped and updated.")
            flight_df["Status"] = Status.COMPLETED.value
            flight_data_handler.update_specific_row(flight_df)

            ''' ERRORS '''
        except FlightDataException as e:
            LOGGER.error(f"Row Name[{flight_df.name}]: {str(e)} ")
            flight_df["Status"] = Status.DATA_ERROR.value
            flight_data_handler.update_specific_row(flight_df)
        except ScrapingDataException as e:
            LOGGER.error(f"Row Name[{flight_df.name}]: {str(e)} ")
            flight_df["Status"] = Status.SCRAPE_ERROR.value
        # except Exception:
        #     LOGGER.error("Got unexpected error. Please contact support")
        #     Browser.quit()
        #     sys.exit()
