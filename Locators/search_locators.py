from selenium.webdriver.common.by import By


class SearchPageLocators:
    SORT_FILTER_DROPDOWN = (
        By.XPATH, "//select[@id='sort-filter-dropdown-SORT']")

    DIRECT_FLIGHT_CHECKBOX = (
        By.XPATH, "//input[contains(@id, 'NUM_OF_STOPS-0')]")
