from Core.webdriver import Browser
from Locators.captcha_locators import CaptchaLocators
from Pages.base_page import BasePage
from Utils.captcha_utils import CaptchaUtils
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class CaptchaPage(BasePage):
    def __init__(self, wait_time):
        LOGGER.info("Initializing Captcha Page Class.")
        super().__init__(wait_time)

    def __click_checkbox(self):
        Browser.default_content()
        frame_el = self.get_element(CaptchaLocators.IFRAME)
        Browser.switch_frame(frame_el)
        self.do_click_with_action(CaptchaLocators.CHECK_BOX)
        Browser.default_content()

    def __request_audio_version(self):
        Browser.default_content()
        images_frame_el = self.get_element(CaptchaLocators.IMAGES_IFRAME)
        Browser.switch_frame(images_frame_el)
        self.do_click_with_action(CaptchaLocators.REQUEST_AUDIO_BUTTON)

    def __solve_audio_captcha(self):
        audio_url = self.get_element_attribute(
            CaptchaLocators.AUDIO_SRC_EL, 'src')
        text = CaptchaUtils.transcribe(audio_url)
        self.send_keys_with_action(CaptchaLocators.AUDIO_RESPONSE_INPUT, text)
        self.do_click_with_action(CaptchaLocators.VERIFY_BUTTON)
        Browser.default_content()
        self.do_click_with_action(CaptchaLocators.CONTINUE_BUTTON)

    def solve_captcha(self):
        LOGGER.info("Solving recaptcha.")
        self.__click_checkbox()
        self.__request_audio_version()
        self.__solve_audio_captcha()
        LOGGER.info("Recaptcha Solved.")
