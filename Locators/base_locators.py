from selenium.webdriver.common.by import By


class BasePageLocators:

    ORIGIN_CLOSE_BTN = (
        By.XPATH, "//div[contains(@class, 'zEiP-origin')]//div[@class='vvTc-item-close']")

    ORIGIN_INPUT = (By.XPATH, "//div[contains(@class, 'zEiP-origin')]//input")

    ORIGIN_SELECT_ITEM = (
        By.XPATH, "//ul[@id='flight-origin-smarty-input-list']//li[1]")

    DESTINATION_CLOSE_BTN = (
        By.XPATH, "//div[contains(@class, 'zEiP-destination')]//div[@class='vvTc-item-close']")

    DESTINATION_INPUT = (
        By.XPATH, "//div[contains(@class, 'zEiP-destination')]//input")

    DESTINATION_SELECT_ITEM = (
        By.XPATH, "//ul[@id='flight-destination-smarty-input-list']//li[1]")

    START_DATE_SPAN = (
        By.XPATH, "//span[@class='sR_k-date' and contains(@aria-label, 'Start')]//span[@class='sR_k-value']")

    NEXT_MONTH_BTN = (By.XPATH, "//button[@aria-label='Next Month']")

    PREVIOUS_MONTH_BTN = (By.XPATH, "//button[@aria-label='Previous month']")

    MONTH_NAME = (By.XPATH, "//div[@class='wHSr-monthName']")

    @staticmethod
    def DATE_PICKER_DAY_BTN(date_str):
        return (
            By.XPATH, f"//div[@aria-label='{date_str}' and not(contains(@class, 'mkUa-isHidden'))]")

    PEAGE_NOTFOUND = (
        By.XPATH, "//div[@class='header-title' and text()='Explore destinations']")
