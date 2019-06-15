from datetime import datetime, timedelta

from pandas import DataFrame

from abtestingstrategiesbackend.agent import Agent
from abtestingstrategiesbackend.email import EmailVariant
from abtestingstrategiesbackend.environment import Environment
from abtestingstrategiesbackend.policy import EpsilonGreedyPolicy
from abtestingstrategiesbackend.rewards.reward_generator import (
    Probability,
    RewardGenerator,
)


def run_experiment(n_emails: int) -> DataFrame:
    reward_probabilities = {
        EmailVariant(10): Probability(0.10),
        EmailVariant(20): Probability(0.20),
        EmailVariant(30): Probability(0.15),
    }
    email_variants = list(reward_probabilities.keys())
    agent = Agent(
        policy=EpsilonGreedyPolicy(
            epsilon=Probability(0.1), email_variants=email_variants
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
