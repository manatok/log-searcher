import re


class TokenisationError(Exception):
    pass


class UnbalancedQuotationsError(TokenisationError):

    def __init__(self, message):
        super().__init__(message)


class UnbalancedParenthesisError(TokenisationError):

    def __init__(self, message):
        super().__init__(message)


class UnknownKeywordError(TokenisationError):

    def __init__(self, message):
        super().__init__(message)


class InvalidExpressionError(TokenisationError):

    def __init__(self, message):
        super().__init__(message)


class TokenTypes:
    AND, OR, NOT, IS, CONTAINS, OPEN_PARENTHESIS, \
        CLOSE_PARENTHESIS, SEARCH_TERM = range(8)


class TokenisedExpression:

    FIELDS = ['browser', 'country', 'url', 'log']
    BOOLEAN_OPERATORS = ['and', 'or', 'not']
    OPERATIONS = ['is', 'contains']
    PARENTHESIS = ['(', ')']
    SEARCH_PLACEHOLDER = 'SEARCH_TERM'

    expression = None
    clean_expression = None
    tokens = []
    terms = None

    position = 0

    def __init__(self, expression: str):
        self.terms = {}
        self.expression = expression
        self.clean()
        self.tokenise()
        self.validate()

    def clean(self):

        def get_and_set_queries(match):
            key = self.SEARCH_PLACEHOLDER + "_" + str(match.start())
            self.terms[key] = match.group()
            return key

        balanced_quotes = r'\"([^\"\\]*(\\.[^\"\\]*)*)\"|\'([^\'\\]*(\\.[^\'\\]*)*)\''

        self.clean_expression = re.sub(
            balanced_quotes, get_and_set_queries, self.expression)

    def tokenise(self):
        reg = re.compile(
            r'(\bAND\b|\bOR\b|\bNOT\b|\band\b|\bor\b|\bnot\b|\bIS\b|\bis\b|\bCONTAINS\b|\bcontains\b|\(|\))')
        self.tokens = reg.split(self.clean_expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

    def validate(self):
        [v() for v in [
            self.validate_quotations,
            self.validate_parenthesis,
            self.validate_allowed_tokens,
            self.validate_dsl]]

        return True

    def validate_quotations(self):
        """
        After the search terms were replaced in the tokenise method
        there should be no more quotes left in the expression.

        :return bool
        :raise UnbalancedQuotationsError
        """
        if "'" in self.clean_expression or '"' in self.clean_expression:
            raise UnbalancedQuotationsError("Error")

        return True

    def validate_parenthesis(self):
        """
        Make sure that the parenthesis are balanced

        :return bool
        :raise UnbalancedParenthesisError
        """
        sequence = [x for x in self.clean_expression if x in '()']

        count = 0
        for parenthesis in sequence:
            if parenthesis == '(':
                count += 1
            else:
                # Trying to close without an open
                if count == 0:
                    raise UnbalancedParenthesisError("Error")

                count -= 1

        # unclosed opens
        if count > 0:
            raise UnbalancedParenthesisError("Error")

        return True

    def validate_allowed_tokens(self):
        """
        Make sure that every token is known and allowed

        :return bool
        :raise UnknownKeywordError
        """
        allowed_keywords = [
            str.lower(x) for x in self.FIELDS + self.OPERATIONS +
            self.BOOLEAN_OPERATORS + self.PARENTHESIS
        ]

        for token in self.tokens:
            if str.lower(token) not in allowed_keywords and \
                    not str.startswith(token, self.SEARCH_PLACEHOLDER):
                raise UnknownKeywordError("Found: " + token)

        return True

    def validate_dsl(self):
        """
        Ensure that the query is grammatically correct.

        :return bool
        :raise InvalidExpressionError
        """
        pass

    def next(self):
        self.position += 1
        return self.tokens[self.position - 1]

    def peek(self):
        return self.tokens[self.position]

    def has_next(self):
        return self.position < len(self.tokens)

    def is_operator(self, value: str):
        return str.lower(value) in self.OPERATIONS

    def is_boolean_operator(self, value: str):
        return self.lower(value) in self.BOOLEAN_OPERATORS

    def is_field(self, value: str):
        return self.lower(value) in self.FIELDS

    def is_open_parenthesis(self, value: str):
        return value == '('

    def is_close_parenthesis(self, value: str):
        return value == ')'
