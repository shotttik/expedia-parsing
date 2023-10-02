from selenium.webdriver.common.by import By


class BasePageLocators:
    @staticmethod
    def DEPARTURE_DATE_BTN(date):
        # return (By.XPATH, f"//div[contains(@aria-label,'{date}')]//..")
        return (By.XPATH, "//button[contains(@aria-label,'{}')]".format(date))

    NEXT_MONTH_BTN = (By.XPATH, "//button[@data-stid='date-picker-paging'][2]")

    DEPART_DATE_DONE_BTN = (
        By.XPATH, "//button[@data-stid='apply-date-picker']")
