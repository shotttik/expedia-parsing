class FlightDataException(Exception):
    def __init__(self, message="Wrong flight data. Skipping.."):
        super().__init__(message)
