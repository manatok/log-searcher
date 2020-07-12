from app.main.dataprovider.log_dataprovider import LogDataProvider
from app.main.model.log import Log


def save_log(data, site_id):
    log = Log(
        message="This is some log",
        browser="Safari",
        country="South Africa",
        url="http://localhost/some/error/path"
    )

    if LogDataProvider.save(log, site_id):
        return {}, 201
    else:
        return {
            'status': 'fail',
            'message': 'Log could not be saved'
        }, 500
