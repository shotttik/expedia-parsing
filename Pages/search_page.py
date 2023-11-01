import pandas as pd
from Core.webdriver import Browser
from Exceptions.DataExceptions import FlightDataException
from Exceptions.VerifyExceptions import VerifyPageException
from Locators.search_locators import SearchPageLocators
from Pages.base_page import BasePage
from Pages.captcha_page import CaptchaPage
from Utils.captcha_utils import CAPTCHA_URL
from Utils.date_utils import DateUtils
from Utils.regex_utils import RegexUtils
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from datetime import timedelta
from selenium.webdriver.common.action_chains import ActionChains
from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)


class SearchPage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing SearchPage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(
            SearchPageLocators.RESULT_COUNT)
        if not result:
            raise VerifyPageException()

    def __wait_result_ready(self):
        LOGGER.info("Waitting results to be found...")
        TEXT = "Results ready."
        result_wait_time = 120
        WebDriverWait(Browser.driver, result_wait_time).until(
            EC.text_to_be_present_in_element(
                SearchPageLocators.RESULT_PROGRESS_DIV, TEXT)
        )

    def check_flights_found(self):
        self.__wait_result_ready()
        LOGGER.info("Checking if flights found...")
        number_flights = int(self.get_element_text(
            SearchPageLocators.RESULT_COUNT))
        if not number_flights:
            raise FlightDataException("Flights not found. Skipping..")

    def choose_cheapest_flights(self):
        LOGGER.info("Choosing cheapest flights.")
        if not self.check_if_element_located(SearchPageLocators.CHEAPEST_BTN):
            raise FlightDataException("No matching flights found. Skipping...")
        self.do_click_with_action(SearchPageLocators.CHEAPEST_BTN)

    def __reset_stops_filter(self):
        LOGGER.info("Reseting stops filter.")
        reset_located = self.check_if_element_located(
            SearchPageLocators.STOPS_FILTER_RESET_BTN)
        if reset_located:
            self.do_click_with_action(
                SearchPageLocators.STOPS_FILTER_RESET_BTN)

    def handle_stops_filter(self, direct):
        LOGGER.info("Handling stops filter.")
        self.scroll_to_element_by_selector(SearchPageLocators.STOPS_HEADER)
        self.__reset_stops_filter()
        if not direct:
            return
        self.hover_to_element(SearchPageLocators.NONSTOPS_LABEL)
        if not self.check_if_element_located(SearchPageLocators.NONSTOPS_ONLY_BTN):
            raise FlightDataException(
                "Direct flight is not available for this countries")
        self.do_click_with_action(SearchPageLocators.NONSTOPS_ONLY_BTN)

    def __reset_times_filter(self):
        LOGGER.info("Reseting times filter.")
        located = self.check_if_element_located(
            SearchPageLocators.TIMES_FILTER_RESET_BTN)
        # if outbound already set we reset it
        if not located:
            return
        self.do_click_with_action(SearchPageLocators.TIMES_FILTER_RESET_BTN)

    def __get_takeoff_times(self):
        # Parse the time range (replace this with your own parsing logic)
        take_off_string = self.get_element_text(
            SearchPageLocators.TIMES_CONTAINER)
        start_time, end_time = RegexUtils.parse_take_off_times(take_off_string)
        # Convert times to minutes since midnight for easier calculation
        start_hours = DateUtils.parse_time(start_time)
        end_hours = DateUtils.parse_time(end_time)
        return start_hours, end_hours

    def handle_outbound(self, outbound: str):
        LOGGER.info('Handling Outbound. Slider logic started...')
        self.scroll_to_element_by_selector(SearchPageLocators.SLIDER_HEADER)
        self.__reset_times_filter()
        slider_width = self.get_element_width(SearchPageLocators.SLIDER_TRACK)

        # Parse the input string 17:00:00 to 5:00 PM
        if type(outbound) == str:
            outbound = DateUtils.string_to_datetime(
                outbound, "%H:%M:%S")
        target_time_string = DateUtils.datetime_to_string(
            outbound, "%I:%M %p")
        start_hours, end_hours = self.__get_takeoff_times()
        target_hours = DateUtils.parse_time(target_time_string)

        # Calculate the target position as a percentage
        target_percentage = (target_hours - start_hours) / \
            (end_hours - start_hours)
        # Calculate the target position on the slider
        target_position = slider_width * target_percentage - 6
        # Use ActionChains to perform the drag-and-drop operation
        try:
            self.move_element_to_right(
                SearchPageLocators.SLIDER_START_BTN, target_position)
        except MoveTargetOutOfBoundsException:
            # moving button of each offset and checking if time is correct
            actions = ActionChains(Browser.driver)
            self.get_element(SearchPageLocators.SLIDER_START_BTN)
            max_right = 0
            while True:
                max_right += 1
                actions.click_and_hold().move_by_offset(
                    1, 0).release().perform()
                start_hours, end_hours = self.__get_takeoff_times()
                if start_hours == target_hours:
                    return
                elif start_hours > target_hours:
                    actions.click_and_hold().move_by_offset(
                        -10, 0).release().perform()
                elif max_right == 400:
                    raise FlightDataException("Outbound exception occured..")

    def __open_seach_form_dialog(self):
        LOGGER.info("Opening search form dialog on clicking trip type button.")
        self.do_click_with_action(SearchPageLocators.TRIP_TYPE_BTN)

    def choose_flight_type(self, return_timestmap):
        LOGGER.info("Choosing flight type.")
        if pd.isna(return_timestmap):
            self.do_click_with_action(
                SearchPageLocators.FLIGHT_TYPE_BTN(oneway=True))
        else:
            self.do_click_with_action(
                SearchPageLocators.FLIGHT_TYPE_BTN(oneway=False))

    def update_search(self):
        LOGGER.info("Updating search page with new configurations.")
        self.do_click_with_action(SearchPageLocators.UPDATE_BUTTON)

    def configure_search_controls(self, flight_df, captcha_page: CaptchaPage):
        self.__open_seach_form_dialog()
        self.choose_flight_type(flight_df["Return"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])
        self.handle_datepicker_and_fill(
            flight_df["Depart"], flight_df["Return"])
        self.update_search()
        # if captcha page solve it
        if Browser.url_contains(CAPTCHA_URL):
            captcha_page.solve_captcha()
        self.handle_if_flight_not_available()
        '''
          check flight found method don't wastes time becaus result element already appeared,
          so we can use it of each filter
        '''
        self.check_flights_found()
        self.choose_cheapest_flights()
        self.handle_outbound(flight_df["Outbound"])
        self.check_flights_found()
        self.handle_stops_filter(flight_df["Direct Flight"])
        self.check_flights_found()
        self.scroll()

    def fetch_cheapest_item_source(self):
        # after clicking it drops down a booking info
        LOGGER.info("Fetching cheapest item container")
        try:
            self.do_click_with_action(SearchPageLocators.FIRST_ITEM_CONTAINER)
            html = self.get_element_source(
                SearchPageLocators.FIRST_ITEM_CONTAINER)
        except:
            raise FlightDataException(
                "Cannot fetch flight item source, maybe flights not available..")
        return html
