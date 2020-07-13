import unittest

from app.service.query_builder.tokeniser import TokenisedExpression, \
    UnbalancedQuotationsError, UnbalancedParenthesisError, UnknownKeywordError


class TokenisedExpressionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    test_quotation_strings = [
        # searching for: application.js
        [""" log contains 'application.js' """, True],
        # searching for: application.js
        [""" log contains "application.js" """, True],
        # searching for: "application.js"
        [""" log contains '"application.js"' """, True],
        # searching for: 'application.js'
        [""" log contains "'application.js'" """, True],
        # searching for: 'application.js'
        [r" log contains '\'application.js\'' ", True],
        # searching for: "application.js"
        [r' log contains "\"application.js\"" ', True],
        # searching for: application.js and something's failed
        [r" log contains 'application.js and something\'s failed ' ", True],
        # searching for: application.js and something"s failed
        [r' log contains "application.js and something\"s failed" ', True],
        # searching for: \
        [r" log contains '\\' ", True],
        # searching for: \
        [r' log contains "\\" ', True],
        # searching for: '\'
        [r" log contains '\'\\\'' ", True],
        # searching for: '\' - evaluates to: log contains '\\'
        [""" log contains '\\\\' """, True],
        # Invalid strings
        [r" log contains '\\'application.js'", False],
        [r' log contains "\\"application.js"', False],
        [r" log contains ''application.js'", False],
        [r' log contains ""application.js"', False]
    ]

    test_parenthesis_strings = [
        [""" ()()() """, True],
        [""" (((((((((()))))((((())))))(((()))))))) """, True],
        [""" (((((((((()))))((((())))))(((())))))))) """, False],
        [""" (((((((((()))))((((())))))(((())))))) """, False],
        [""" (log contains 'foo' AND (country is 'South Africa' OR country is 'Malta')) """, True],
        [""" some unbalanced ()) expression """, False],
        [""" (log contains 'foo)' AND (country is '(South Africa' OR country is 'Malta')) """, True],
        [""" (log contains 'foo)' AND (country is 'South Africa' OR country is 'Malta') """, False]
    ]

    test_token_strings = [
        [""" country contains 'foo' """, True],
        [""" browser (country) (url) (log) is contains and or not () """, True],
        [""" [] """, False],
        [""" unknown words """, False]
    ]

    def test_quotation_validation(self):
        for i, quotation_test in enumerate(self.test_quotation_strings):
            with self.subTest(i):
                quotation_string, is_valid = quotation_test

                if not is_valid:
                    with self.assertRaises(UnbalancedQuotationsError):
                        TokenisedExpression(quotation_string)
                else:
                    TokenisedExpression(quotation_string)

    def test_parenthesis_validation(self):

        for i, parenthesis_test in enumerate(self.test_parenthesis_strings):
            with self.subTest(i):
                parenthesis_string, is_valid = parenthesis_test

                if not is_valid:
                    with self.assertRaises(UnbalancedParenthesisError):
                        TokenisedExpression(parenthesis_string)
                else:
                    TokenisedExpression(parenthesis_string)

    def test_token_validation(self):

        for i, token_test in enumerate(self.test_token_strings):
            with self.subTest(i):
                token_string, is_valid = token_test

                if not is_valid:
                    with self.assertRaises(UnknownKeywordError):
                        TokenisedExpression(token_string)
                else:
                    TokenisedExpression(token_string)
