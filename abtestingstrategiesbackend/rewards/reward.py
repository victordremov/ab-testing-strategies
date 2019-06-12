from dataclasses import dataclass
from datetime import datetime

from abtestingstrategiesbackend.email import Email


@dataclass(frozen=True)
class Reward:
    value: float
    cause: Email
    reward_datetime: datetime