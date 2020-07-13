from app.model.log import Log
from flask import current_app
from elasticsearch import Elasticsearch


def create_index_if_not_exists(index):

    if not LogDataProvider.get_es_connection().indices.exists(index):

        # index settings
        settings = {
            "mappings": {
                "properties": {
                    "url": {
                        "type": "text"
                    },
                    "country": {
                        "type": "keyword"
                    },
                    "message": {
                        "type": "text"
                    },
                    "browser": {
                        "type": "keyword"
                    }
                }
            }
        }

        # create index
        LogDataProvider.get_es_connection().indices.create(
            index=index, ignore=400, body=settings)


class LogDataProvider:
    @staticmethod
    def get_es_connection():
        if not hasattr(current_app, 'es') or not current_app.es:
            print("Creating")
            current_app.es = Elasticsearch(
                [current_app.config['ELASTICSEARCH_URL']])

        return current_app.es

    @staticmethod
    def save(log: Log, site_id: str):
        create_index_if_not_exists(site_id)

        payload = {}
        for field in log.__annotations__.keys():
            payload[field] = getattr(log, field)

        resp = LogDataProvider.get_es_connection().index(
            index=site_id, body=payload)

        return 'result' in resp and resp['result'] == 'created'

    @staticmethod
    def query(query_string: str, site_id: str):
        create_index_if_not_exists(site_id)
        res = LogDataProvider.get_es_connection().search(
            index=site_id, body=query_string)

        hits = []
        for hit in res['hits']['hits']:
            hits.append(hit['_source'])

        return hits
