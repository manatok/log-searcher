from .tokenised_expression import TokenisedExpression, TokenisationError


class BooleanCondition(object):
    """
    BooleanCondition represents a leaf node in the boolean
    expression tree.

    key = Elasticsearch column
    value: The search value
    operation: contains | is
    negate: if we are to negate this condition
    """
    key = ""
    value = ""
    operation = ""
    negate = False


class BooleanNode(object):
    """
    BooleanNode represents a boolean (AND | OR) that
    is to be performed on a it's two child branches.

    node_type: and | or
    left & right:  BooleanNode | BooleanCondition
    negate: If this node is to be negated
    """
    node_type = ""
    left = None
    right = None
    negate = False

    def __init__(self, node_type: str):
        self.node_type = node_type


class BooleanExpressionGenerator:
    """
    BooleanExpressionGenerator constructs a Boolean
    Expression Tree, given a tokenised expression.
    The tree is constructed in a recursive manner as
    each of the tokens are evaluated.
    """
    b_tree = None
    tokens = None

    def __init__(self, tokenised_expression: TokenisedExpression):
        self.tokens = tokenised_expression

    def build(self):
        self.boolean_tree = self.parse_expression()
        return self.boolean_tree

    def parse_expression(self):
        first_and = self.parse_and()

        while self.tokens.has_next() and str.lower(self.tokens.peek()) == 'or':
            self.tokens.next()
            next_and = self.parse_and()
            next_node = BooleanNode('or')
            next_node.left = first_and
            next_node.right = next_and
            first_and = next_node

        return first_and

    def parse_and(self):
        first_condition = self.parse_condition()

        while self.tokens.has_next() and str.lower(self.tokens.peek()) == 'and':
            self.tokens.next()
            next_condition = self.parse_condition()
            next_node = BooleanNode('and')
            next_node.left = first_condition
            next_node.right = next_condition
            first_condition = next_node

        return first_condition

    def parse_condition(self):
        negate = False
        if self.tokens.has_next() and str.lower(self.tokens.peek()) == 'not':
            self.tokens.next()
            negate = True

        if self.tokens.has_next() and self.tokens.peek() == '(':
            self.tokens.next()
            expression = self.parse_expression()
            expression.negate = negate

            if self.tokens.has_next() and self.tokens.peek() == ')':
                self.tokens.next()
                return expression
            else:
                raise Exception("Closing ) expected, but got " +
                                self.tokens.next())

        condition = BooleanCondition()
        condition.negate = negate

        if self.tokens.has_next():
            condition.key = self.tokens.next()
        else:
            raise TokenisationError("Incomplete condition")

        if self.tokens.has_next():
            condition.operation = self.tokens.next()
        else:
            raise TokenisationError("Incomplete condition")

        if self.tokens.has_next() and str.lower(self.tokens.peek()) == 'not':
            condition.negate = not condition.negate
            self.tokens.next()

        if self.tokens.has_next():
            condition.value = self.tokens.terms[self.tokens.next()]
        else:
            raise TokenisationError("Missing Value")

        return condition
