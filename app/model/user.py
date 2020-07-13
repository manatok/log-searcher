from dataclasses import dataclass
from typing import List


@dataclass
class User:
    id: str
    email: str
    password: str
    allowed_site_ids: List[str]

    def check_password(self, password):
        return password == self.password
