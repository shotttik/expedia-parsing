from enum import Enum


class Status(Enum):
    PENDING = 0
    COMPLETED = 1
    DATA_ERROR = 2
    SCRAPE_ERROR = 3
