import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from Core.webdriver import Browser
from selenium.common.exceptions import TimeoutException
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class CorePage:
    def __init__(self, wait_time):
        self.wait_time = wait_time
        self.actions = ActionChains(Browser.driver)

    def get_title(self, title):
        LOGGER.info('Getting title from current page.')
        WebDriverWait(Browser.driver,
                      self.wait_time).until(EC.title_is(title))
        return Browser.driver.title

    def wait_all_element_located(self, by_locator: tuple):
        LOGGER.info('Waitting specific elements to be located')
        WebDriverWait(Browser.driver, self.wait_time).until(
            EC.visibility_of_all_elements_located(by_locator))

    def wait_for_element_to_dissapear(self, by_locator: tuple):
        LOGGER.info('Waitting element to be dissapear.')
        WebDriverWait(Browser.driver, self.wait_time).until(
            EC.invisibility_of_element_located(by_locator))

    def verify_page_by_element(self, by_locator: tuple):
        LOGGER.info('Verifing page by element.')
        element = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.visibility_of_all_elements_located(by_locator)
        )
        return bool(element)

    def get_element_text(self, by_locator: tuple):
        LOGGER.info('Getting element text.')
        element = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.visibility_of_element_located(by_locator)
        )
        return element.text

    def wait_text_to_be_present_in_element(self, by_locator: tuple, text):
        element = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.text_to_be_present_in_element(by_locator, text)
        )
        return element

    def verify_page_by_url_params(self, filter_name):
        LOGGER.info('Verifing page by filter name.')
        return f'?filter={filter_name}' in Browser.driver.current_url

    def scroll(self, page_split):
        LOGGER.info('Scrolling to page split.')

        Browser.driver.execute_script(
            f"window.scrollTo(0, document.body.scrollHeight/{page_split});")

    def check_if_alert_exist(self):
        LOGGER.info('Checking Alert Existing.')
        alert_exist = True
        try:
            WebDriverWait(Browser.driver, self.wait_time/4).until(
                EC.alert_is_present())
        except:
            alert_exist = False
        return alert_exist

    def open_link_in_new_tab(self, url):
        LOGGER.info(f'Opening link in new tab URL: {url}')
        Browser.driver.execute_script(f"window.open('{url}');")
        Browser.change_window_by_id(1)

    def scroll_to_element_by_selector(self, selector):
        LOGGER.info('Scrolling to element by selector.')
        el = self.get_element(selector)
        self.scroll_to_element(el)

    def scroll_to_element(self, el):
        LOGGER.info('Scrolling to element.')
        Browser.driver.execute_script(
            "arguments[0].scrollIntoView(true);", el)

    def wait_url_changing(self):
        LOGGER.info('Waiting until url changes.')
        WebDriverWait(Browser.driver, self.wait_time).until(
            EC.url_changes(Browser.driver.current_url))

    def wait_element_to_be_clickable(self, selector):
        LOGGER.info('Waiting element to be clickable.')
        WebDriverWait(Browser.driver, self.wait_time).until(
            EC.element_to_be_clickable(selector))

    def do_click_with_action(self, selector):
        LOGGER.info("Doing click with action.")
        el = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_element_located(selector))
        self.actions.move_to_element(el)
        self.actions.pause(random.uniform(1, 5))
        self.actions.click()
        self.actions.pause(random.uniform(1, 5))
        self.actions.perform()

    def send_keys_with_action(self, selector, text: str):
        LOGGER.info("Sending keys with action chains.")
        el = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.visibility_of_element_located(selector)
        )
        self.actions.click(on_element=el)
        self.actions.pause(random.uniform(1, 5))
        self.actions.send_keys(text)
        self.actions.pause(random.uniform(1, 5))
        self.actions.perform()

    def wait_elements_to_appear(self, selector):
        LOGGER.info("Wait elements to appear..")
        WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_all_elements_located(selector))

    def check_if_element_located(self, selector) -> bool:
        LOGGER.info("Checking element located in page.")
        try:
            WebDriverWait(Browser.driver, self.wait_time).until(
                EC.presence_of_element_located(selector))
            return True
        except:
            return False

    def check_if_input_selected(self, selector) -> bool:
        LOGGER.info("Checking if input element checked.")
        input_el = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_element_located(selector))
        return input_el.is_selected()

    def get_item_elements(self, selector):
        LOGGER.info("Getting item elements.")
        items = []
        try:
            items = WebDriverWait(Browser.driver, self.wait_time).until(
                EC.presence_of_all_elements_located(selector))
        except TimeoutException:
            LOGGER.info("Items not found.")
        finally:
            return items

    def get_element(self, selector):
        LOGGER.info("Getting element.")
        el = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_element_located(selector))
        return el

    def click_to_element(self, element):
        LOGGER.info("Clicking to element.")
        self.actions.click(on_element=element)
        self.actions.pause(random.uniform(1, 5))
        self.actions.perform()

    def get_element_width(self, selector):
        LOGGER.info("Getting element width.")
        element = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_element_located(selector))
        return element.size['width']

    def move_element_to_right(self, selector, target_position):
        LOGGER.info("Moving element to right.")
        btn = self.get_element(selector)
        self.actions.click_and_hold(btn)
        self.actions.move_by_offset(target_position, 0)
        self.actions.release().perform()

    def hover_to_element(self, selector):
        LOGGER.info("Hovering to element")
        el = self.get_element(selector)
        self.actions.move_to_element(el)
        self.actions.perform()

    def get_element_source(self, selector) -> str:
        LOGGER.info("Getting element html source")
        element = WebDriverWait(Browser.driver, self.wait_time).until(
            EC.presence_of_element_located(selector))
        return element.get_attribute('innerHTML')
