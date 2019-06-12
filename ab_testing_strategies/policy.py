import random
from abc import ABC, abstractmethod
from collections import Iterable

from dataclasses import dataclass
from typing import Dict, Union, Tuple, Iterator
import numpy as np

from ab_testing_strategies.email import EmailVariant, Email
from ab_testing_strategies.rewards.reward import Reward
from ab_testing_strategies.rewards.reward_generator import Probability


@dataclass
class EmailVariantStatistics:
    n_attempts: int
    n_successes: int

    @property
    def probability(self) -> Probability:
        try:
            p = Probability(self.n_successes / self.n_attempts)
        except ZeroDivisionError:
            p = Probability(0.0)
        return p


class UnknownEvent(ValueError):
    pass


class Policy(ABC):
    @abstractmethod
    def update_statistics(self, event: Union[Email, Reward]) -> None:
        pass

    @abstractmethod
    def choose_email_variant(self) -> EmailVariant:
        pass


class EpsilonGreedyPolicy(Policy):
    def __init__(
        self, epsilon: Probability, email_variants: Iterator[EmailVariant]
    ) -> None:
        if not isinstance(epsilon, Probability):
            epsilon = Probability(epsilon)
        self.epsilon = epsilon
        self.email_variants = list(email_variants)
        self.email_variants_statistics: Dict[EmailVariant, EmailVariantStatistics] = {}
        for email_variant in iter(self.email_variants):
            self.email_variants_statistics[email_variant] = EmailVariantStatistics(
                n_attempts=0, n_successes=0
            )

    def update_statistics(self, event: Union[Email, Reward]) -> None:
        if isinstance(event, Email):
            self._increment_n_attempts(event.variant)
        elif isinstance(event, Reward):
            self._increment_n_succeses(event.cause.variant)
        else:
            msg = (
                f"Cannot update policy statistics."
                f" Instance of `Email` and `Reward` expected,"
                f" but {event} of type {type(event)} given."
            )
            raise UnknownEvent(msg)

    def choose_email_variant(self) -> EmailVariant:
        if np.random.binomial(1, p=self.epsilon) == 1:
            return self._choose_random_variant()
        return self._choose_currently_best_variant()

    def _increment_n_attempts(self, email_variant: EmailVariant) -> None:
        self.email_variants_statistics[email_variant].n_attempts += 1

    def _increment_n_succeses(self, email_variant: EmailVariant) -> None:
        self.email_variants_statistics[email_variant].n_successes += 1

    def _choose_currently_best_variant(self) -> EmailVariant:
        # noinspection PyTypeChecker
        currently_best_variant_statistics: Tuple[
            EmailVariant, EmailVariantStatistics
        ] = max(
            self.email_variants_statistics.items(),
            key=lambda key_value_pair: key_value_pair[1].probability,
        )
        best_email_variant = currently_best_variant_statistics[0]
        return best_email_variant

    def _choose_random_variant(self) -> EmailVariant:
        return random.choice(self.email_variants)
