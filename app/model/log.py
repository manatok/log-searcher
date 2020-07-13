from dataclasses import dataclass


@dataclass
class Log:
    message: str
    browser: str
    url: str
    country: str
