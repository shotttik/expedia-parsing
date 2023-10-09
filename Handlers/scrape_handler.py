from bs4 import BeautifulSoup
from Exceptions.ScrapingExceptions import ScrapingDataException
from logger import CustomLogger
LOGGER = CustomLogger.get_logger(__name__)


class ScrapeDataHandler:
    def __init__(self, html=None):
        """
        Parse html with BeautifulSoup
        """
        LOGGER.info("Initializing ScrapeDataHandler class.")
        self.soup = None  # Initialize the soup attribute as None

        if html:
            self.parse_html(html)

    def parse_html(self, html):
        """
        Parse the provided HTML and set the soup attribute
        """
        self.soup = BeautifulSoup(html, "html.parser")

    @property
    def price(self):
        LOGGER.info("Parsing Price.")
        soup_el_list = self.soup.select('div[class*=price-text-container]')
        if not soup_el_list:
            raise ScrapingDataException("Price couldn't find..")
        p = [0].div.text
        return p

    @property
    def times(self):
        LOGGER.info("Parsing Times.")
        soup_el_list = self.soup.select('div[class*=mod-variant-large]')
        if not soup_el_list:
            raise ScrapingDataException("Times Dep\Arri couldn't find..")
        spans = soup_el_list[0].find_all('span')
        time_dep = spans[0].text
        time_arriv = spans[2].text
        return time_dep, time_arriv

    @property
    def airline(self):
        LOGGER.info("Parsing airline.")
        el = self.soup.find('div', {'dir': 'auto'}).get_text(strip=True)
        return el

    @property
    def provider(self):
        LOGGER.info("Parsing provider.")
        providers_list = self.soup.select('div[class*=provider-name]')
        if not providers_list:
            raise ScrapingDataException("Times Dep\Arri couldn't find..")
        provider = providers_list[1].div.text
        return provider

    def get_data(self) -> dict:
        time_dep, time_arriv = self.times
        info_dict = {"Price": self.price,
                     "Airline": self.airline,
                     "Time Dep": time_dep,
                     "Time Arrive": time_arriv,
                     "Provider": self.provider}
        return info_dict
