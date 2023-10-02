class VerifyPageException(Exception):
    def __init__(self, message="Verification of page failed..."):
        super().__init__(message)
