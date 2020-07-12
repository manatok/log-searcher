
test_sites = [
    {
        "id": "site1",
        "scheme": "http",
        "domain": "localhost",
        "max_requests": 10,
        "window_seconds": 60
    },
    {
        "id": "site2",
        "scheme": "http",
        "domain": "localhost",
        "max_requests": 5,
        "window_seconds": 60
    }
]


class Site:
    id = None
    scheme = None
    domain = None
    max_requests = 0
    window_seconds = 0

    def __init__(self, id: str, scheme: str, domain: str,
                 max_requests: int, window_seconds: int):
        self.id = id
        self.scheme = scheme
        self.domain = domain
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    @staticmethod
    def get_by_id(id: str):
        for site in test_sites:
            if site['id'] == id:
                return Site(site["id"], site["scheme"], site["domain"],
                            site["max_requests"], site["window_seconds"])

        return None
