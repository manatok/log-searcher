
from dataclasses import dataclass


@dataclass
class Site:
    id: str
    scheme: str
    domain: str
    max_requests: int = 0
    window_seconds: int = 0
