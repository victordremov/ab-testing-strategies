import random
from datetime import timedelta
from typing import Dict, Any, Union, Callable, Optional

import numpy as np

from abtestingstrategiesbackend.email import EmailVariant, Email
from abtestingstrategiesbackend.rewards.reward import Reward


class OutOfRangeException(ValueError):
    def __init__(self, min_value: float, max_value: float, given_value: float, msg: str):
        self.min_value = min_value
        self.max_value = max_value
        self.given_value = given_value


class Probability(float):
    def __init__(self, x: Union[float, int, str]) -> None:
        super().__init__()
        min_value = 0.0
        max_value = 1.0
        if x < min_value or x > max_value:
            raise OutOfRangeException(
                min_value=min_value,
                max_value=max_value,
                given_value=x,
                msg=f"Probability must be from f{min_value} to {max_value} inclusively, got {x}."
            )


class UnknownEmailVariantError(KeyError):
    pass


class RewardGenerator:
    def __init__(
        self,
        reward_probabilities: Dict[EmailVariant, Probability],
        generate_reward_delay: Callable[[], timedelta],
    ):
        self._reward_probabilities: Dict[EmailVariant, Probability] = {}
        for email_variant, probability in reward_probabilities.items():
            self._reward_probabilities[EmailVariant(email_variant)] = Probability(
                probability
            )
        self._generate_reward_delay: Callable[[], timedelta] = generate_reward_delay

    def generate(self, email: Email) -> Optional[Reward]:
        try:
            reward_probability = self._reward_probabilities[email.variant]
        except KeyError as e:
            msg = f"Email variant {email.variant} must be one of {self._reward_probabilities.keys()}"
            raise UnknownEmailVariantError(msg) from e
        reward_value = np.random.binomial(1, reward_probability)
        if reward_value > 0:
            reward_delay = self._generate_reward_delay()
            reward = Reward(reward_value, email, email.sending_datetime + reward_delay)
            return reward
