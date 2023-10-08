import sys
from Core.webdriver import Browser
from Exceptions.DataExceptions import FlightDataException
from Exceptions.DateExceptions import DepartureDateRequiredException
from Exceptions.InputExceptions import InputTextRequiredException
from Exceptions.VerifyExceptions import VerifyPageException
from .base_page import BasePage
from Locators.home_locators import HomePageLocators
import pandas as pd
from selenium.common.exceptions import TimeoutException
from Utils.date_utils import DateUtils
from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)


class HomePage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing HomePage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(
            HomePageLocators.HOME_TITLE)
        if not result:
            raise VerifyPageException()

    def check_direct_flights(self, check: int):
        LOGGER.info("Checking Direct flights checkbox.")
        if not check:
            return
        located = self.check_if_element_located(
            HomePageLocators.DIRECT_FLIGHT_INPUT)
        if check and not located:
            raise FlightDataException(
                "Direct flight on this trip not available...")
        self.do_click_with_action(HomePageLocators.DIRECT_FLIGHT_INPUT)

    def change_flight_type(self, return_date):
        LOGGER.info("Changing flight type.")
        self.do_click_with_action(HomePageLocators.TRIP_TYPE_MENU_SPAN)

        if pd.isna(return_date):
            self.do_click_with_action(
                HomePageLocators.FLIGHT_TYPE_BTN(one_way=True))
        else:
            self.do_click_with_action(
                HomePageLocators.FLIGHT_TYPE_BTN(one_way=False))

    def configure_search_controls(self, flight_df: pd.DataFrame):
        LOGGER.info("Started configuration of search controls.")
        self.change_flight_type(flight_df["Return"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])
        self.handle_datepicker_and_fill(
            flight_df["Depart"], flight_df["Return"])
        self.check_direct_flights(flight_df["Direct Flight"])

    def go_to_search_page(self):
        LOGGER.info("Clicking to search button")
        self.do_click_with_action(HomePageLocators.SEARCH_BTN)
