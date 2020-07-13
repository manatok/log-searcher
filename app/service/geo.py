import urllib.request
import json


def get_country(ip: str):
    with urllib.request.urlopen("https://geolocation-db.com/json/" + ip) as url:
        data = json.loads(url.read().decode())
        return data['country_name']
