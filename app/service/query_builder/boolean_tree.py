from .tokeniser import TokenisedExpression


class BooleanCondition(object):
    key = ""
    value = ""
    operation = ""
    negate = False

    def __getattribute__(self, name):
        if name == 'left':
            return BooleanNode(object.__getattribute__(self, 'key'))
        elif name == 'right':
            negate_str = ""
            if object.__getattribute__(self, 'negate'):
                negate_str = "NOT "
            return BooleanNode(negate_str + object.__getattribute__(self, 'value'))
        elif name == 'val':
            return BooleanNode(object.__getattribute__(self, 'operation')).node_type
        else:
            return object.__getattribute__(self, name)


class BooleanNode(object):
    # AND | OR
    node_type = ""
    left = None
    right = None
    negate = False

    def __init__(self, node_type: str):
        self.node_type = node_type

    def __getattribute__(self, name):
        if name == 'val':
            negate_str = ""
            if object.__getattribute__(self, 'negate'):
                negate_str = "NOT "
            return negate_str + object.__getattribute__(self, 'node_type')
        else:
            return object.__getattribute__(self, name)


class BooleanExpressionGenerator:

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

            if self.tokens.has_next():
                condition.operation = self.tokens.next()

                if self.tokens.has_next() and str.lower(self.tokens.peek()) == 'not':
                    condition.negate = not condition.negate
                    self.tokens.next()

                if self.tokens.has_next():
                    condition.value = self.tokens.terms[self.tokens.next()]
                else:
                    raise Exception("Missing Value")
            else:
                raise Exception("Incomplete condition")
        else:
            raise Exception("Incomplete condition")

        return condition
