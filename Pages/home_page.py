from Exceptions.VerifyExceptions import VerifyException
from .base_page import BasePage
from Locators.home_locators import HomePageLocators
from logger import CustomLogger
import pandas as pd
LOGGER = CustomLogger.get_logger(__name__)


class HomePage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing HomePage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(HomePageLocators.HOME_ICON)
        if not result:
            raise VerifyException()

    def check_direct_flights(self, check: int):
        LOGGER.info("Checking Direct flights checkbox.")
        if not check:
            return
        self.do_click_with_action(HomePageLocators.DIRECT_INPUT)

    def configure_search_controls(self, flight_df: pd.DataFrame):
        LOGGER.info("Started configuration of search controls.")
        self.check_direct_flights(flight_df["Direct Flight"])
