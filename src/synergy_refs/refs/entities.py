from typing import (
    List,
    Iterable,
)
from enum import Enum, auto
from dataclasses import dataclass, field


class RefLevel(Enum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 5
    V6 = 6


@dataclass
class User:
    pk: str
    ref_level: RefLevel = RefLevel.V1
    team_size: int = 0

    balance: int = 120

    refs: List["User"] = field(default_factory=list)
    ref_pks: List[str] = field(default_factory=list)



@dataclass
class UserGraph:
    root: User

    @property
    def users(self) -> Iterable[User]:
        yield from self._iter_over_subtree(self.root)

    def _iter_over_subtree(self, user: User) -> Iterable[User]:
        yield user

        for ref in user.refs:
            yield from self._iter_over_subtree(ref)

