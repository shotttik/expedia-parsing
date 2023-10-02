from Exceptions.VerifyExceptions import VerifyPageException
from Locators.home_locators import HomePageLocators
from Locators.search_locators import SearchPageLocators
from Pages.base_page import BasePage
from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)


class SearchPage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing SearchPage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(
            SearchPageLocators.SORT_FILTER_DROPDOWN)
        if not result:
            raise VerifyPageException()

    def check_direct_flight(self, direct_flight):
        LOGGER.info("Checking direct flight.")
        if not direct_flight:
            return
        if self.check_if_element_located(SearchPageLocators.DIRECT_FLIGHT_CHECKBOX):
            self.do_click_with_action(
                SearchPageLocators.DIRECT_FLIGHT_CHECKBOX)
