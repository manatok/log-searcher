from app.dataprovider.log_dataprovider import LogDataProvider
from app.model.log import Log
from .geo import get_country
from .query_builder.tokenised_expression import TokenisedExpression
from .query_builder.boolean_tree import BooleanExpressionGenerator
from .query_builder.es_adapter import ElasticsearchAdapter
from werkzeug.exceptions import BadRequest


class TokenisationError(BadRequest):
    error_code = 400

    def __init__(self, message):
        super().__init__(message, self.error_code)


def save_log(data, site_id: str, browser: str, url: str, ip: str):
    """
    Save the log record to Elasticsearch
    """
    # Construct the entity to be saved
    log = Log(data['message'], browser, get_country(ip), url)

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
    es_adapter = ElasticsearchAdapter(boolean_tree)
    return LogDataProvider.query(
        es_adapter.get_query(limit, offset),
        site_id
    )
