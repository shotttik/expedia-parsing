import pandas as pd
from Exceptions.InputExceptions import InputNotFoundException, InputTextRequiredException
from Exceptions.VerifyExceptions import VerifyPageException
from Locators.home_locators import HomePageLocators
from Locators.search_locators import SearchPageLocators
from Pages.base_page import BasePage
from Utils.date_utils import DateUtils
from Utils.regex_utils import RegexUtils
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

    def choose_cheapest_flights(self):
        LOGGER.info("Choosing cheapest flights.")
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
        self.__reset_stops_filter()
        if not direct:
            return
        self.hover_to_element(SearchPageLocators.NONSTOPS_LABEL)
        self.do_click_with_action(SearchPageLocators.NONSTOPS_ONLY_BTN)

    def __reset_times_filter(self):
        LOGGER.info("Reseting times filter.")
        located = self.check_if_element_located(
            SearchPageLocators.TIMES_FILTER_RESET_BTN)
        # if outbound already set we reset it
        if not located:
            return
        self.do_click_with_action(SearchPageLocators.TIMES_FILTER_RESET_BTN)

    def handle_outbound(self, outbound: str):
        LOGGER.info('Handling Outbound. Slider logic started...')
        self.__reset_times_filter()
        slider_width = self.get_element_width(SearchPageLocators.SLIDER_TRACK)

        # Parse the time range (replace this with your own parsing logic)
        take_off_string = self.get_element_text(
            SearchPageLocators.TIMES_CONTAINER)
        start_time, end_time = RegexUtils.parse_take_off_times(take_off_string)

        # Parse the input string 17:00:00 to 5:00 PM
        if type(outbound) == str:
            outbound = DateUtils.string_to_datetime(
                outbound, "%H:%M:%S")
        target_time_string = DateUtils.datetime_to_string(
            outbound, "%I:%M %p")

        # Convert times to minutes since midnight for easier calculation
        start_hours = DateUtils.parse_time(start_time)
        end_hours = DateUtils.parse_time(end_time)
        target_hours = DateUtils.parse_time(target_time_string)

        # Calculate the target position as a percentage
        target_percentage = (target_hours - start_hours) / \
            (end_hours - start_hours)
        # Calculate the target position on the slider
        target_position = slider_width * target_percentage - 6
        # Use ActionChains to perform the drag-and-drop operation
        self.move_element_to_right(
            SearchPageLocators.SLIDER_START_BTN, target_position)

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

    def configure_search_controls(self, flight_df):
        self.__open_seach_form_dialog()
        self.choose_flight_type(flight_df["Return"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])
        self.handle_datepicker_and_fill(
            flight_df["Depart"], flight_df["Return"])
        self.update_search()
        self.handle_if_flight_not_found()
        self.choose_cheapest_flights()
        self.handle_outbound(flight_df["Outbound"])
        self.handle_stops_filter(flight_df["Direct Flight"])
