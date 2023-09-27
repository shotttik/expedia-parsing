from webdriver import Browser
from config import config_browser, get_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Pages.home_page import HomePage

if '__main__' == __name__:
    # Configuring browser
    config_browser_data = config_browser()
    browser_i = Browser(config_browser_data)
    WebDriverWait(browser_i.driver, browser_i.wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
    )
    data = get_data()
    Browser.getDriver().get(data['start_url'])
    main_page = HomePage(browser_i.wait_time)
    main_page.verify_page()
    Browser.quit()
    # main_page.go_to_parsing_page()
