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

    def reset_times_filter(self):
        LOGGER.info("reseting times filter.")
        located = self.check_if_element_located(
            SearchPageLocators.TIMES_FILTER_RESET_BTN)
        # if outbound already set we reset it
        if not located:
            return
        self.do_click_with_action(SearchPageLocators.TIMES_FILTER_RESET_BTN)

    def handle_outbound(self, outbound: str):
        LOGGER.info('Handling Outbound. Slider logic started...')
        self.reset_times_filter()
        slider_width = self.get_element_width(SearchPageLocators.SLIDER_TRACK)

        # Parse the time range (replace this with your own parsing logic)
        take_off_string = self.get_element_text(
            SearchPageLocators.TIMES_CONTAINER)
        start_time, end_time = RegexUtils.parse_take_off_times(take_off_string)

        # Parse the input string 17:00:00 to 5:00 PM
        target_datetime = DateUtils.string_to_datetime(outbound, "%H:%M:%S")
        target_time_string = DateUtils.datetime_to_string(
            target_datetime, "%I:%M %p")

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
