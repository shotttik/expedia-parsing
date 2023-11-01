from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class Browser():
    __instance = None

    def __new__(cls, config_browser):

        if cls.__instance is None:
            LOGGER.info("Creating Browser class instance.")
            cls.__instance = super(Browser, cls).__new__(cls)
            cls.browser = config_browser["browser"]
            cls.wait_time = config_browser["wait_time"]
            LOGGER.info("Configurating Browser.")
            chrome_options = webdriver.ChromeOptions()

            [
                chrome_options.add_argument(argument)
                for argument in config_browser["arguments"]
            ]

            experimental_options = config_browser["experimental_options"]
            [
                chrome_options.add_experimental_option(
                    option[0], option[1]) for option in experimental_options
            ]
            if config_browser["browser"] == 'chrome':
                cls.__instance.driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=chrome_options)
            elif config_browser["browser"] == 'firefox':
                cls.__instance.driver = webdriver.Firefox(service=Service(
                    GeckoDriverManager().install()), options=chrome_options)
            else:
                # Sorry, we can't help you right now.
                assert ("Support for Firefox or Remote only!")

        return cls.__instance

    @classmethod
    @property
    def driver(cls):
        if cls.__instance is None:
            raise ValueError(
                "Instance not created yet.")
        return cls.__instance.driver

    @classmethod
    def change_window_by_id(cls, id):
        LOGGER.info(f'Changing browser windows ID: {id}.')
        cls.driver.switch_to.window(
            cls.driver.window_handles[id])

    @classmethod
    def close_current_window(cls):
        LOGGER.info('Closing current Window.')
        cls.driver.close()

    @classmethod
    def save_screenshot(cls, filename="screenshot.png"):
        LOGGER.info("Saving screenshot as " + filename)
        cls.driver.save_screenshot(filename)

    @classmethod
    def back(cls):
        LOGGER.info('Browser back.')
        cls.driver.back()

    @classmethod
    def default_content(cls):
        LOGGER.info("Switching to default content.")
        cls.driver.switch_to.default_content()

    @classmethod
    def switch_frame(cls, el):
        LOGGER.info("Switching to frame.")
        cls.driver.switch_to.frame(el)

    @classmethod
    def url_contains(cls, text: str) -> bool:
        LOGGER.info(f"Checking url contains {text} .")
        return text in cls.driver.current_url

    @classmethod
    def quit(cls):
        LOGGER.info("Quitting Browser.")
        return cls.driver.quit()
