from selenium.webdriver.common.by import By


class HomePageLocators:

    HOME_ICON = (
        By.XPATH, "//div[@class='Homepage_searchControlInnerContainer__ZmEwY']")

    ORIGIN_INPUT = (By.XPATH, "//input[@id='originInput-input']")

    DESTINATION_INPUT = (By.XPATH, "//input[@id='destinationInput-input']")

    DIRECT_INPUT = (By.XPATH, "//input[@name='prefer-directs']")
