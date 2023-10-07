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

    def __open_date_picker(self):
        LOGGER.info("Opening date picker...")
        self.do_click_with_action(HomePageLocators.START_DATE_SPAN)

    def fill_origin_input(self, text):
        LOGGER.info("Filling origin input with text")
        if pd.isna(text):
            raise InputTextRequiredException
        origin_selected_close_btns = self.get_item_elements(
            HomePageLocators.ORIGIN_CLOSE_BTN)
        for item in origin_selected_close_btns:
            self.click_to_element(item)
            LOGGER.info("All selected origin items removed..")
        self.send_keys_with_action(HomePageLocators.ORIGIN_INPUT, text)
        located = self.check_if_element_located(
            HomePageLocators.ORIGIN_SELECT_ITEM)
        if not located:
            raise FlightDataException("Origin country not found. Skipping..")
        self.do_click_with_action(
            HomePageLocators.ORIGIN_SELECT_ITEM)

    def fill_destination_input(self, text):
        LOGGER.info("Filling destination input with text")
        if pd.isna(text):
            raise InputTextRequiredException
        destination_selected_close_btns = self.get_item_elements(
            HomePageLocators.DESTINATION_CLOSE_BTN)
        for item in destination_selected_close_btns:
            self.click_to_element(item)
            LOGGER.info("All selected destination items removed..")
        self.send_keys_with_action(HomePageLocators.DESTINATION_INPUT, text)
        located = self.check_if_element_located(
            HomePageLocators.DESTINATION_SELECT_ITEM)
        if not located:
            raise FlightDataException(
                "Destination country not found. Skipping...")
        self.do_click_with_action(
            HomePageLocators.DESTINATION_SELECT_ITEM)

    def choose_date(self, flight_timestamp):
        LOGGER.info('Choosing flight date.')
        # Format the datetime object as "Tuesday, October 10, 2023"
        # date = DateUtils.timestamp_to_date(timestamp, "%A, %B %d, %Y")
        # Format the timestamp ex. 2023-11-22 00:00:00 object as "22 Oct 2023"
        # Depart Date
        flight_date = DateUtils.timestamp_to_datetime(flight_timestamp)
        flight_string = DateUtils.datetime_to_string(flight_date)
        # Current Date
        current_datepicker_string = self.get_element_text(
            HomePageLocators.MONTH_NAME)
        current_datepicker_datetime = DateUtils.string_to_datetime(
            current_datepicker_string)
        while True:
            try:
                self.do_click_with_action(
                    HomePageLocators.DATE_PICKER_DAY_BTN(flight_string))
                break
            except TimeoutException:
                LOGGER.info('Day not found.')
                # logic click next button or back button
                if flight_date > current_datepicker_datetime:
                    self.do_click_with_action(
                        HomePageLocators.NEXT_MONTH_BTN)
                else:
                    self.do_click_with_action(
                        HomePageLocators.PREVIOUS_MONTH_BTN)

    def handle_datepicker_and_fill(self, depart_timestamp, return_timestamp):
        LOGGER.info("Handling datepicker and filling with data.")
        self.__open_date_picker()
        if pd.isna(depart_timestamp):
            raise DepartureDateRequiredException
        self.choose_date(depart_timestamp)
        if not pd.isna(return_timestamp):
            self.choose_date(return_timestamp)
        # datetime picker automatically close

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
