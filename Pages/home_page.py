from Exceptions.VerifyExceptions import VerifyException
from webdriver import Browser
from .base_page import BasePage
from Locators.home_locators import HomePageLocators


class HomePage(BasePage):

    def __init__(self, wait_time):
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(HomePageLocators.HOME_ICON)
        if not result:
            raise VerifyException()
