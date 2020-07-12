from app.main.dataprovider.log_dataprovider import LogDataProvider
from app.main.model.log import Log
from .geo import get_country


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
