import pandas as pd
from Core.webdriver import Browser
from Exceptions.DataExceptions import FlightDataException
from Exceptions.DateExceptions import DepartureDateRequiredException
from Exceptions.InputExceptions import InputTextRequiredException
from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from Locators.base_locators import BasePageLocators
from Locators.home_locators import HomePageLocators
from Pages.core_page import CorePage
from Utils.date_utils import DateUtils
from selenium.webdriver.common.action_chains import ActionChains
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class BasePage(CorePage):
    def __init__(self, wait_time):
        LOGGER.info("Initializing HomePage Class.")
        super().__init__(wait_time)

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
        try:
            self.do_click_with_action(
                HomePageLocators.ORIGIN_SELECT_ITEM)
        except MoveTargetOutOfBoundsException:
            # if this error ocured , country already choosen so we skip it
            pass

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
        try:
            self.do_click_with_action(
                HomePageLocators.DESTINATION_SELECT_ITEM)
        except MoveTargetOutOfBoundsException:
            # if this error ocured , country already choosen so we skip it
            pass

    def choose_date(self, flight_timestamp):
        LOGGER.info('Choosing flight date.')
        # Format the datetime object as "Tuesday, October 10, 2023"
        # date = DateUtils.timestamp_to_date(timestamp, "%A, %B %d, %Y")
        # Format the timestamp ex. 2023-11-22 00:00:00 object as "22 Oct 2023"
        flight_date = DateUtils.timestamp_to_datetime(flight_timestamp)
        # Depart Date
        flight_string = DateUtils.datetime_to_string(flight_date)
        # Current Date
        try:
            current_datepicker_string = self.get_element_text(
                HomePageLocators.MONTH_NAME)
        except TimeoutException:
            LOGGER.info(
                "Datepicker already closed, because of choosing same date as previous row.")
            return
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

    def __open_date_picker(self):
        LOGGER.info("Opening date picker...")
        self.do_click_with_action(HomePageLocators.START_DATE_SPAN)
        # datetime picker automatically close

    def handle_datepicker_and_fill(self, depart_timestamp, return_timestamp):
        LOGGER.info("Handling datepicker and filling with data.")
        self.__open_date_picker()
        if pd.isna(depart_timestamp):
            raise DepartureDateRequiredException
        self.choose_date(depart_timestamp)
        if not pd.isna(return_timestamp):
            self.choose_date(return_timestamp)

    # checks if flights is not available in countries
    def handle_if_flight_not_available(self):
        LOGGER.info(
            "Handling if flight not available and not found page appeared.")
        located = self.check_if_element_located(
            BasePageLocators.PEAGE_NOTFOUND)
        if located:
            Browser.back()
            raise FlightDataException
