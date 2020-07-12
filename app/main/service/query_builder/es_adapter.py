import ast
import json
from .boolean_tree import BooleanNode, BooleanCondition


class ElasticsearchAdapter:

    boolean_tree = None

    OPERATION_MAPPING = {
        'is': 'term',
        'contains': 'match'
    }

    BOOL_MAPPING = {
        'or': 'should',
        'and': 'must',
        'negate': 'must_not'
    }

    def __init__(self, boolean_tree: BooleanNode):
        self.boolean_tree = boolean_tree

    def get_query(self):
        query = {
            'query': self.get_query_recursive(self.boolean_tree)
        }
        return json.dumps(query)

    def get_query_recursive(self, node):

        # we are at a leaf node
        if isinstance(node, BooleanCondition):
            search_dict = {}
            search_dict[self.OPERATION_MAPPING[node.operation]] = {
                node.key: ast.literal_eval(node.value)
            }
        else:
            left = self.get_query_recursive(node.left)
            right = self.get_query_recursive(node.right)
            search_dict = {
                "bool": {
                    self.BOOL_MAPPING[str.lower(node.node_type)]: [left, right]
                }
            }

        if node.negate:
            return {
                "bool": {
                    "must_not": search_dict
                }
            }
        else:
            return search_dict
