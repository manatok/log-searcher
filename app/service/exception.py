from werkzeug.exceptions import BadRequest


class TokenisationError(BadRequest):
    error_code = 400

    def __init__(self, message):
        super().__init__(message, self.error_code)


class UnbalancedQuotationsError(TokenisationError):
    pass


class UnbalancedParenthesisError(TokenisationError):
    pass


class UnknownKeywordError(TokenisationError):
    pass


class InvalidExpressionError(TokenisationError):
    pass


class RateLimitExceededError(BadRequest):
    error_code = 400

    def __init__(self, message):
        super().__init__(message, self.error_code)
