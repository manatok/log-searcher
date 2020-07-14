import unittest
import json
from app.service.query_builder.tokenised_expression import TokenisedExpression
from app.service.query_builder.boolean_tree import BooleanExpressionGenerator
from app.service.query_builder.es_adapter import ElasticsearchAdapter


class ESQueryTestCase(unittest.TestCase):

    test_tree_strings = [
        {
            "expression": """ country is 'South Africa' """,
            "expected_query": '{"term": {"country": "South Africa"}}'
        },
        {
            "expression": """ (country is 'South Africa') """,
            "expected_query": '{"term": {"country": "South Africa"}}'
        },
        {
            "expression": """ NOT country is 'South Africa' """,
            "expected_query": '{"bool": {"must_not": {"term": {"country": "South Africa"}}}}'
        },
        {
            "expression": """ country is 'South Africa' and url contains 'sheep' """,
            "expected_query": '{"bool": {"must": [{"term": {"country": "South Africa"}}, {"match": {"url": "sheep"}}]}}'
        },
        {
            "expression": """ country is 'South Africa' and url contains 'sheep' and url contains 'foo' """,
            "expected_query": '{"bool": {"must": [{"bool": {"must": [{"term": {"country": "South Africa"}}, {"match": {"url": "sheep"}}]}}, {"match": {"url": "foo"}}]}}'
        },
        {
            "expression": """ country is 'South Africa' and (url contains 'sheep') """,
            "expected_query": '{"bool": {"must": [{"term": {"country": "South Africa"}}, {"match": {"url": "sheep"}}]}}'
        },
        {
            "expression": """ country is 'South Africa' and NOT (url contains 'sheep') """,
            "expected_query": '{"bool": {"must": [{"term": {"country": "South Africa"}}, {"bool": {"must_not": {"match": {"url": "sheep"}}}}]}}'
        },
        {
            "expression": """ (country is 'South Africa') and (url contains 'sheep' or country contains 'Africa') """,
            "expected_query": '{"bool": {"must": [{"term": {"country": "South Africa"}}, {"bool": {"should": [{"match": {"url": "sheep"}}, {"match": {"country": "Africa"}}]}}]}}'
        },
        {
            "expression": """ not country is 'Big Africa' or NOT (url contains 'sheep' and NOT (country contains 'Africa' and browser is 'Chrome')) """,
            "expected_query": '{"bool": {"should": [{"bool": {"must_not": {"term": {"country": "Big Africa"}}}}, {"bool": {"must_not": {"bool": {"must": [{"match": {"url": "sheep"}}, {"bool": {"must_not": {"bool": {"must": [{"match": {"country": "Africa"}}, {"term": {"browser": "Chrome"}}]}}}}]}}}}]}}'
        },
        {
            "expression": """ (country is 'South Africa' and url contains 'www.boo.com') or browser is 'Chrome 4.x.8' """,
            "expected_query": '{"bool": {"should": [{"bool": {"must": [{"term": {"country": "South Africa"}}, {"match": {"url": "www.boo.com"}}]}}, {"term": {"browser": "Chrome 4.x.8"}}]}}'
        },
        {
            "expression": """ ((country is 'South Africa' and url contains 'www.boo.com') or browser is 'Chrome 4.x.8') and not browser contains 'Explorer' """,
            "expected_query": '{"bool": {"must": [{"bool": {"should": [{"bool": {"must": [{"term": {"country": "South Africa"}}, {"match": {"url": "www.boo.com"}}]}}, {"term": {"browser": "Chrome 4.x.8"}}]}}, {"bool": {"must_not": {"match": {"browser": "Explorer"}}}}]}}'
        }
    ]

    def test_boolean_tree(self):
        """
        Ensure that the given query expression is converted into the correct
        Elasticsearch query.
        """
        for i, tree_test in enumerate(self.test_tree_strings):
            with self.subTest(i):
                tokeniser = TokenisedExpression(tree_test['expression'])
                boolean_tree = BooleanExpressionGenerator(tokeniser)
                tree = boolean_tree.build()
                adapter = ElasticsearchAdapter(tree)
                query = adapter.get_query(limit=10, offset=0)
                query_json = json.loads(query)
                expected_json = json.loads(tree_test['expected_query'])
                self.assertEqual(
                    expected_json, query_json['query'])
