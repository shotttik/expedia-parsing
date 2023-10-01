class InputTextRequiredException(Exception):
    def __init__(self, message="Input text cannot be null or empty string..."):
        super().__init__(message)
