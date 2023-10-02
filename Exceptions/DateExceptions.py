class DepartureDateRequiredException(Exception):
    def __init__(self, message="Departure date is required..."):
        super().__init__(message)
