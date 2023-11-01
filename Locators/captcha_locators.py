from selenium.webdriver.common.by import By


class CaptchaLocators:
    IFRAME = (By.XPATH, ".//iframe[@title='reCAPTCHA']")

    CHECK_BOX = (By.ID, "recaptcha-anchor-label")

    IMAGES_IFRAME = (
        By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']")

    REQUEST_AUDIO_BUTTON = (By.ID, "recaptcha-audio-button")

    AUDIO_SRC_EL = (
        By.ID, "audio-source")

    AUDIO_RESPONSE_INPUT = (By.ID, "audio-response")

    VERIFY_BUTTON = (By.ID, "recaptcha-verify-button")

    CONTINUE_BUTTON = (
        By.XPATH, "//div[@id='main']//button[contains(@class, 'Button-No-Standard-Style')]")
