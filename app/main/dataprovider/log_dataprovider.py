import json
from app.main.model.log import Log
from flask import current_app


def create_index_if_not_exists(index):
    if not current_app.es:
        return False

    if not current_app.es.indices.exists(index):

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
        current_app.es.indices.create(
            index=index, ignore=400, body=settings)


class LogDataProvider:
    @staticmethod
    def save(log: Log, site_id: str):
        create_index_if_not_exists(site_id)

        payload = {}
        for field in log.__annotations__.keys():
            payload[field] = getattr(log, field)

        resp = current_app.es.index(index=site_id, body=payload)

        return 'result' in resp and resp['result'] == 'created'

    @staticmethod
    def query(query_string: str, site_id: str):
        create_index_if_not_exists(site_id)
        res = current_app.es.search(index=site_id, body=query_string)

        hits = []
        for hit in res['hits']['hits']:
            hits.append(hit['_source'])

        return hits
