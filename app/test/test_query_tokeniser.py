import unittest

from app.service.query_builder.tokenised_expression import TokenisedExpression, \
    TokenisationError


class TokenisedExpressionTestCase(unittest.TestCase):

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

    """
    Test if the parenthesis are balanced.
    Need to ignore the parenthesis inside the search phrase.
    """
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

    """
    Test that only valid keywords and terms are used.
    """
    test_token_strings = [
        [""" country contains 'foo' """, True],
        [""" browser (country) (url) (message) is contains and or not () """, True],
        [""" [] """, False],
        [""" unknown words """, False]
    ]

    def test_quotation_validation(self):
        """
        Test various combinations of quotations to ensure that they are
        escaped properly and that the correct number of search terms 
        are found.
        """
        for i, quotation_test in enumerate(self.test_quotation_strings):
            with self.subTest(i):
                quotation_string, is_valid, total_tokens = quotation_test

                if not is_valid:
                    with self.assertRaises(TokenisationError):
                        TokenisedExpression(quotation_string)
                else:
                    te = TokenisedExpression(quotation_string)

                    # Make sure the regex finds the correct number of terms
                    self.assertEqual(total_tokens, len(te.terms.keys()))

    def test_parenthesis_validation(self):
        """
        Ensure that all of the parenthesis outside of the search terms
        are balanced.
        """
        for i, parenthesis_test in enumerate(self.test_parenthesis_strings):
            with self.subTest(i):
                parenthesis_string, is_valid = parenthesis_test

                if not is_valid:
                    with self.assertRaises(TokenisationError):
                        TokenisedExpression(parenthesis_string)
                else:
                    TokenisedExpression(parenthesis_string)

    def test_token_validation(self):
        """
        Test that only valid keywords and terms are used.
        """
        for i, token_test in enumerate(self.test_token_strings):
            with self.subTest(i):
                token_string, is_valid = token_test

                if not is_valid:
                    with self.assertRaises(TokenisationError):
                        TokenisedExpression(token_string)
                else:
                    TokenisedExpression(token_string)
