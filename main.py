import sys

import pandas as pd
from Core.webdriver import Browser
from Core.config import config_browser, get_data
from Exceptions.DataExceptions import FlightDataException
from Exceptions.ScrapingExceptions import ScrapingDataException
from Handlers.flight_data_handler import FlightDataHandler
from Handlers.scrape_handler import ScrapeDataHandler
from Pages.captcha_page import CaptchaPage
from Pages.home_page import HomePage
from Pages.search_page import SearchPage
from Utils.captcha_utils import CAPTCHA_URL
from enums.StatusEnums import Status

from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)

if '__main__' == __name__:
    '''Configuring browser'''
    config_browser_data = config_browser()
    browser_i = Browser(config_browser_data)
    data = get_data()
    flight_data_handler = FlightDataHandler(
        data["flights_input_file"], data["flights_output_file"])
    first_flight_scraping = True
    home_page = HomePage(browser_i.wait_time)
    search_page = SearchPage(browser_i.wait_time)
    captcha_page = CaptchaPage(browser_i.wait_time)
    scraper = ScrapeDataHandler()
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
                home_page.verify_page()
                home_page.accept_cookies()
                # loading excel to dataframe
                home_page.configure_search_controls(flight_df)
                home_page.go_to_search_page()
                Browser.close_current_window()
                # when clicking search opens a new window
                Browser.change_window_by_id(0)
                # if captcha page solve it
                if Browser.url_contains(CAPTCHA_URL):
                    captcha_page.solve_captcha()
                '''Search Page'''
                search_page.handle_if_flight_not_available()
                '''
                if flights not found it will skip and don't waste time for configuring other search filters
                thats why used a this method a few times
                '''
                search_page.check_flights_found()
                search_page.verify_page()
                search_page.choose_cheapest_flights()
                search_page.handle_outbound(flight_df["Outbound"])
                search_page.check_flights_found()
                first_flight_scraping = False
            else:
                search_page.configure_search_controls(flight_df, captcha_page)

            ''' SCRAPING '''
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
            # avoids to return home page and initialize it again
            if first_flight_scraping:
                first_flight_scraping = False
            flight_data_handler.update_specific_row(flight_df)
        except ScrapingDataException as e:
            LOGGER.error(f"Row Name[{flight_df.name}]: {str(e)} ")
            flight_df["Status"] = Status.SCRAPE_ERROR.value
        except Exception as e:
            import time
            time.sleep(300)
            LOGGER.exception(
                f"Unexpected error occurred while processing row [{flight_df.name}]")
            Browser.quit()
            sys.exit()
