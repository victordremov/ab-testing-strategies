from datetime import datetime, timedelta

from pandas import DataFrame

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
    environment = Environment(
        agent=agent,
        reward_generator=RewardGenerator(
            reward_probabilities=reward_probabilities,
            generate_reward_delay=lambda: timedelta(hours=1),
        ),
        start_datetime=start_datetime,
    )
    for _ in range(n_emails):
        environment.process_email_sending()
    reward_over_sent_count = environment.statistics.get_reward_over_sent_count_data()
    return reward_over_sent_count
