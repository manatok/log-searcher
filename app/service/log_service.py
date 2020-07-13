from app.dataprovider.log_dataprovider import LogDataProvider
from app.model.log import Log
# from app.util.print_b_tree import printBTree
from .geo import get_country
from .query_builder.tokeniser import TokenisedExpression
from .query_builder.boolean_tree import BooleanExpressionGenerator
from .query_builder.es_adapter import ElasticsearchAdapter


def save_log(data, site_id: str, browser: str, url: str, ip: str):

    country = get_country(ip)

    log = Log(
        message=data['message'],
        browser=browser,
        country=country,
        url=url
    )

    if LogDataProvider.save(log, site_id):
        return {}, 201
    else:
        return {
            'status': 'fail',
            'message': 'Log could not be saved'
        }, 500


def query_logs(query: str, site_id: str, limit: int, offset: int):

    tokenised_expression = TokenisedExpression(query)
    boolean_expression = BooleanExpressionGenerator(tokenised_expression)
    boolean_tree = boolean_expression.build()
    # printBTree(boolean_tree, lambda n: (str(n.val), n.left, n.right))
    es_adapter = ElasticsearchAdapter(boolean_tree)
    return LogDataProvider.query(
        es_adapter.get_query(limit, offset),
        site_id
    )
