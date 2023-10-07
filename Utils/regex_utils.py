import re
from Exceptions.RegexExceptions import TakeOffStringRequiredException
from logger import CustomLogger

LOGGER = CustomLogger.get_logger(__name__)


class RegexUtils:

    @staticmethod
    def parse_take_off_times(string: str) -> tuple:
        pattern = r'(\d{1,2}:\d{2} [APM]{2})'
        matches = re.findall(pattern, string)
        if len(matches) == 2:
            start_time = matches[0]  # Extract the start time
            end_time = matches[1]    # Extract the end time
            return start_time, end_time
        else:
            raise TakeOffStringRequiredException
