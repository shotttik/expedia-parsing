from logger import CustomLogger
import datetime
LOGGER = CustomLogger.get_logger(__name__)


class DateUtils:
    DATE_FORMAT = "%d.%m.%Y"
    FULL_DATE_FORMAT = "%A %B %d, %Y"
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
        return datetime.datetime.strptime(date_str, format)

    @classmethod
    def datetime_to_string(cls, dt, format=FULL_DATE_FORMAT):
        if format != cls.FULL_DATE_FORMAT:
            return dt.strftime(format)
        # instead of this 'Thursday February 01, 2024' returning this 'Thursday February 1, 2024'
        return dt.strftime(cls.FULL_DATE_FORMAT).replace(
            dt.strftime("%d"), cls.format_day(dt.strftime("%d")))

    @staticmethod
    def get_month_name(dt: datetime.datetime) -> str:
        return dt.strftime('%B')

    # Convert times to hours (12-hour format)
    def parse_time(time_str):
        time_parts = time_str.split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1].split()[0])
        if "PM" in time_str and hours != 12:
            hours += 12
        return hours + minutes / 60.0

    def format_day(day):
        return str(int(day))

    @classmethod
    def pd_dateparse(cls, x):
        return datetime.datetime.strftime(x.to_pydatetime(), cls.DATE_FORMAT)
