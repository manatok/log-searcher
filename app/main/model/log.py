from dataclasses import dataclass


@dataclass
class Log:
    id: str
    message: str
    browser: str
    url: str
    country: str
