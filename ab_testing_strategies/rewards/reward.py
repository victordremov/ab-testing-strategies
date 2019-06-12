from dataclasses import dataclass
from datetime import datetime

from ab_testing_strategies.email import Email


@dataclass(frozen=True)
class Reward:
    value: float
    cause: Email
    reward_datetime: datetime