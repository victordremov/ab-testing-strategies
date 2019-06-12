from collections import Hashable

from dataclasses import dataclass
from datetime import datetime

from typing import Optional


class EmailVariant(int):
    pass


@dataclass
class Email:
    sending_datetime: datetime
    variant: Optional[EmailVariant] = None
