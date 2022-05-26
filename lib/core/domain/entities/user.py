from dataclasses import dataclass, asdict, astuple
from typing import Dict


@dataclass(frozen=True, order=True)
class User:
    id: int
    name: str
    last_name: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_tuple(self) -> tuple:
        return astuple(self)

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)
