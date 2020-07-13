import re
from werkzeug.exceptions import BadRequest


class TokenisationError(BadRequest):
    error_code = 400

    def __init__(self, message):
        super().__init__(message, self.error_code)


class TokenisedExpression:
    """
    TokenisedExpression converts a search query string into a tokenised
    representation. There are three main stages:

    1. Clean: creates a version of the query expression without any search
        terms in it, they are all replaced by placeholders. This allows
        for easier validation and tokenisation.

    2. Tokenise: splits the search query into it's token constituents.

    3. Validate: ensures that the query is escaped properly, that all of the
            parenthesis are balanced and that the tokens are all allowed.
    """

    FIELDS = ['browser', 'country', 'url', 'message']
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
        """
        Replace all of the search terms with placeholders
        """
        def get_and_set_queries(match):
            key = self.SEARCH_PLACEHOLDER + "_" + str(match.start())
            self.terms[key] = match.group()
            return key

        # used to find all search phrases surrounded by single or double quotes
        balanced_quotes = r'\"([^\"\\]*(\\.[^\"\\]*)*)\"|\'([^\'\\]*(\\.[^\'\\]*)*)\''

        self.clean_expression = re.sub(
            balanced_quotes, get_and_set_queries, self.expression)

    def tokenise(self):
        """
        Split the query expression into all of its tokens.
        """
        reg = re.compile(
            r'(\bAND\b|\bOR\b|\bNOT\b|\band\b|\bor\b|\bnot\b|\bIS\b|\bis\b|\bCONTAINS\b|\bcontains\b|\(|\))')
        self.tokens = reg.split(self.clean_expression)
        self.tokens = [t.strip() for t in self.tokens if t.strip() != '']

    def validate(self):
        """
        Ensure that the query is valid by running all the checks

        :raise TokenisationError
        """
        [v() for v in [
            self.validate_quotations,
            self.validate_parenthesis,
            self.validate_allowed_tokens]]

        return True

    def validate_quotations(self):
        """
        After the search terms were replaced in the tokenise method
        there should be no more quotes left in the expression.

        :return bool
        :raise TokenisationError
        """
        if "'" in self.clean_expression or '"' in self.clean_expression:
            raise TokenisationError(
                "Unbalanced quotations in the query")

        return True

    def validate_parenthesis(self):
        """
        Make sure that the parenthesis are balanced

        :return bool
        :raise TokenisationError
        """
        sequence = [x for x in self.clean_expression if x in '()']

        count = 0
        for parenthesis in sequence:
            if parenthesis == '(':
                count += 1
            else:
                # Trying to close without an open
                if count == 0:
                    raise TokenisationError(
                        "Too many closing parenthesis in the query")

                count -= 1

        # unclosed opens
        if count > 0:
            raise TokenisationError(
                "Unclosed parenthesis in the query")

        return True

    def validate_allowed_tokens(self):
        """
        Make sure that every token is known and allowed

        :return bool
        :raise TokenisationError
        """
        allowed_keywords = [
            str.lower(x) for x in self.FIELDS + self.OPERATIONS +
            self.BOOLEAN_OPERATORS + self.PARENTHESIS
        ]

        for token in self.tokens:
            if str.lower(token) not in allowed_keywords and \
                    not str.startswith(token, self.SEARCH_PLACEHOLDER):
                raise TokenisationError("Unexpected keyword: " + token)

        return True

    def next(self):
        self.position += 1
        return self.tokens[self.position - 1]

    def peek(self):
        return self.tokens[self.position]

    def has_next(self):
        return self.position < len(self.tokens)
