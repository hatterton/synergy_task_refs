from django.db import models

from enum import Enum, auto
from typing import List
from dataclasses import dataclass, field

class RefLevel(Enum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 5
    V6 = 6

# Create your models here.

@dataclass
class User:
    pk: str
    ref_level: RefLevel = RefLevel.V1
    team_size: int = 0

    balance: int = 120

    refs: List["User"] = field(default_factory=list)


@dataclass
class UserGraph:
    root: User
