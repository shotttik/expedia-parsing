class InputTextRequiredException(Exception):
    def __init__(self, message="Input text cannot be null or empty string..."):
        super().__init__(message)


class InputNotFoundException(Exception):
    def __init__(self, message="Input element not found.") -> None:
        super().__init__(message)
