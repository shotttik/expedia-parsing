from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class DateUtils:
    @staticmethod
    def timestamp_to_date(timestamp, format):
        return timestamp.to_pydatetime().strftime(format)
