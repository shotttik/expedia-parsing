from datetime import datetime
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class DateUtils:
    MONTH_NAMES = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]

    @staticmethod
    def timestamp_to_datetime(timestamp):
        return timestamp.to_pydatetime()

    # example format "November 2023" to datetime
    @staticmethod
    def string_to_datetime(date_str, format='%B %Y'):
        return datetime.strptime(date_str, format)

    @staticmethod
    def datetime_to_string(dt, format='%A %B %d, %Y'):
        return dt.strftime(format)

    @staticmethod
    def get_month_name(dt: datetime) -> str:
        return dt.strftime('%B')
