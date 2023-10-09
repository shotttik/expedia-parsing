class ScrapingDataException(Exception):
    def __init__(self, message="Scraping Data exception, couldn't find element.."):
        super().__init__(message)
