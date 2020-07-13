from dataclasses import dataclass
from typing import List


@dataclass
class TokenUser:
    id: str
    allowed_site_ids: List[str]
