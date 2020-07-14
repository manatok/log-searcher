from app.dataprovider.log_dataprovider import LogDataProvider
from app.model.log import Log
from .geo import get_country
from .query_builder.tokenised_expression import TokenisedExpression
from .query_builder.boolean_tree import BooleanExpressionGenerator
from .query_builder.es_adapter import ElasticsearchAdapter
from werkzeug.exceptions import InternalServerError


def save_log(data: str, site_id: str, browser: str, url: str, ip: str):
    """
    Save the log record to Elasticsearch
    """
    # Construct the entity to be saved
    log = Log(data['message'], browser, url, get_country(ip))

    if LogDataProvider.save(log, site_id):
        return
    else:
        return InternalServerError('Log could not be saved')


def query_logs(query: str, site_id: str, limit: int, offset: int):
    # convert query string into tokens
    tokenised_expression = TokenisedExpression(query)
    # construst boolean expression tree
    boolean_expression = BooleanExpressionGenerator(tokenised_expression)
    boolean_tree = boolean_expression.build()
    # generate Elasticsearch query from expression tree
    es_adapter = ElasticsearchAdapter(boolean_tree)

    # run the query
    return LogDataProvider.query(
        es_adapter.get_query(limit, offset),
        site_id
    )
