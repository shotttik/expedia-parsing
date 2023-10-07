class TakeOffStringRequiredException(Exception):
    def __init__(self, message="Take off string is not found..."):
        super().__init__(message)
