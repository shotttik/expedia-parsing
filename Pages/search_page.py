from Exceptions.InputExceptions import InputNotFoundException, InputTextRequiredException
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
            SearchPageLocators.RESULT_COUNT)
        if not result:
            raise VerifyPageException()

    def check_direct_flight(self, direct_flight):
        LOGGER.info("Checking direct flight.")
        if direct_flight == None:
            return
        if not self.check_if_element_located(SearchPageLocators.DIRECT_FLIGHT_CHECKBOX):
            raise InputNotFoundException

        checked = self.check_if_input_selected(
            SearchPageLocators.DIRECT_FLIGHT_CHECKBOX)
        if checked != bool(direct_flight):
            self.do_click_with_action(
                SearchPageLocators.DIRECT_FLIGHT_CHECKBOX)

    def fill_origin_input(self, text: str):
        LOGGER.info("Filling origin input with text")
        if not text:
            raise InputTextRequiredException
        self.do_click_with_action(SearchPageLocators.ORIGIN_BTN)
        self.send_keys_with_action(SearchPageLocators.ORIGIN_INPUT, text)
        self.wait_elements_to_appear(
            SearchPageLocators.ORIGIN_RESULT_ITEM_BTN)
        self.do_click_with_action(
            SearchPageLocators.ORIGIN_RESULT_ITEM_BTN)

    def fill_destination_input(self, text: str):
        LOGGER.info("Filling destination input with text")
        if not text:
            raise InputTextRequiredException
        self.do_click_with_action(SearchPageLocators.DESTINATION_BTN)
        self.send_keys_with_action(SearchPageLocators.DESTINATION_INPUT, text)
        self.wait_elements_to_appear(
            SearchPageLocators.DESTINATION_RESULT_ITEM_BTN)
        self.do_click_with_action(
            SearchPageLocators.DESTINATION_RESULT_ITEM_BTN)

    def change_flight_type(self, return_date):
        LOGGER.info("Changing flight type.")
        self.do_click_with_action(SearchPageLocators.FLIGHT_TYPE_MENU_BTN)
        if not return_date:
            self.do_click_with_action(
                SearchPageLocators.FLIGHT_TYPE_BTN(one_way=True))
        else:
            self.do_click_with_action(
                SearchPageLocators.FLIGHT_TYPE_BTN(one_way=False))

    def update_search_controls(self, flight_df):
        self.check_direct_flight(flight_df["Direct Flight"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])
        self.change_flight_type(flight_df["Return"])
        # @TODO left to choose dates logicly
