from datetime import datetime, timedelta

import pkg_resources
from numpy.core.multiarray import ndarray
from pandas import DataFrame
import numpy as np
import pandas as pd
from typing import Iterator

from abtestingstrategiesbackend.agent import Agent
from abtestingstrategiesbackend.email import EmailVariant
from abtestingstrategiesbackend.environment import Environment
from abtestingstrategiesbackend.policy import EpsilonGreedyPolicy, ABTestingPolicy
from abtestingstrategiesbackend.rewards.reward_generator import (
    Probability,
    RewardGenerator,
)


def run_ab_testing_experiment(
    n_emails: int, probability_a: float, probability_b: float, n_emails_for_ab_test: int
) -> DataFrame:
    variant_A = EmailVariant(1)
    variant_B = EmailVariant(2)
    reward_probabilities = {
        variant_A: Probability(probability_a),
        variant_B: Probability(probability_b),
    }
    email_variants = list(reward_probabilities.keys())
    agent = Agent(
        policy=ABTestingPolicy(
            email_variants=email_variants, n_emails_for_ab_test=n_emails_for_ab_test
        )
    )
    start_datetime = datetime(2019, 1, 1)

    class RewardDelaySampler:
        def __init__(self, values: ndarray, probabilities: ndarray) -> None:
            self.values = values
            self.probabilities = probabilities

        def __call__(self):
            return pd.to_timedelta(np.random.choice(self.values, size=1, p=self.probabilities))

    csv_file = pkg_resources.resource_filename('abtestingstrategiesbackend.resources', 'timespan_from_send_to_click_with_probability.csv')
    reward_delay_distribution = pd.read_csv(csv_file)
    reward_delay_values = pd.to_timedelta(reward_delay_distribution['MinutesSinceSend'], unit='m')
    reward_delay_probabilities = reward_delay_distribution['probability']
    reward_delay_sampler = RewardDelaySampler(values=reward_delay_values, probabilities=reward_delay_probabilities)

    environment = Environment(
        agent=agent,
        reward_generator=RewardGenerator(
            reward_probabilities=reward_probabilities,
            generate_reward_delay=reward_delay_sampler
        ),
        start_datetime=start_datetime,
    )
    for _ in range(n_emails):
        environment.process_email_sending()
    reward_over_sent_count = environment.statistics.get_reward_over_sent_count_data()
    return reward_over_sent_count