import unittest

from app.service.query_builder.tokeniser import TokenisedExpression, \
    UnbalancedQuotationsError, UnbalancedParenthesisError, UnknownKeywordError


class TokenisedExpressionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    """
    The string to test in the following format:
    [test_string, is_valid, total_seach_tokens]
    """
    test_quotation_strings = [
        # searching for: application.js
        [""" message contains 'application.js' """, True, 1],
        # searching for: application.js
        [""" message contains "application.js" """, True, 1],
        [""" message contains 'application.js' and browser is 'Chrome' """, True, 2],
        # searching for: "application.js"
        [""" message contains '"application.js"' """, True, 1],
        # searching for: 'application.js'
        [""" message contains "'application.js'" """, True, 1],
        # searching for: 'application.js'
        [r" message contains '\'application.js\'' ", True, 1],
        # searching for: "application.js"
        [r' message contains "\"application.js\"" ', True, 1],
        # searching for: application.js and something's failed
        [r" message contains 'application.js and something\'s failed ' ", True, 1],
        # searching for: application.js and something"s failed
        [r' message contains "application.js and something\"s failed" ', True, 1],
        # searching for: \
        [r" message contains '\\' ", True, 1],
        # searching for: \
        [r' message contains "\\" ', True, 1],
        # searching for: '\'
        [r" message contains '\'\\\'' ", True, 1],
        # searching for: '\' - evaluates to: message contains '\\'
        [""" message contains '\\\\' """, True, 1],
        # Invalid strings
        [r" message contains '\\'application.js'", False, None],
        [r' message contains "\\"application.js"', False, None],
        [r" message contains ''application.js'", False, None],
        [r' message contains ""application.js"', False, None]
    ]

    test_parenthesis_strings = [
        [""" ()()() """, True],
        [""" (((((((((()))))((((())))))(((()))))))) """, True],
        [""" (((((((((()))))((((())))))(((())))))))) """, False],
        [""" (((((((((()))))((((())))))(((())))))) """, False],
        [""" (message contains 'foo' AND (country is 'South Africa' OR country is 'Malta')) """, True],
        [""" some unbalanced ()) expression """, False],
        [""" (message contains 'foo)' AND (country is '(South Africa' OR country is 'Malta')) """, True],
        [""" (message contains 'foo)' AND (country is 'South Africa' OR country is 'Malta') """, False]
    ]

    test_token_strings = [
        [""" country contains 'foo' """, True],
        [""" browser (country) (url) (message) is contains and or not () """, True],
        [""" [] """, False],
        [""" unknown words """, False]
    ]

    def test_quotation_validation(self):
        for i, quotation_test in enumerate(self.test_quotation_strings):
            with self.subTest(i):
                quotation_string, is_valid, total_tokens = quotation_test

                if not is_valid:
                    with self.assertRaises(UnbalancedQuotationsError):
                        TokenisedExpression(quotation_string)
                else:
                    te = TokenisedExpression(quotation_string)

                    # Make sure the regex finds the correct number of terms
                    self.assertEqual(total_tokens, len(te.terms.keys()))

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
