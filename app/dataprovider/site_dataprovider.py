from app.model.site import Site

# This is just for demo purposes and would ultimately live in the database
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


def get_site_by_id(id: str) -> Site:
    """
    This is just a demo function for getting a Site entity.
    This would be replaced when integrating with a real DB.
    """
    for site in test_sites:
        if site['id'] == id:
            return Site(site["id"], site["scheme"], site["domain"],
                        site["max_requests"], site["window_seconds"])

    return None
