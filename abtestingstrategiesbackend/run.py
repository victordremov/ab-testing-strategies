from datetime import datetime, timedelta

from abtestingstrategiesbackend.agent import Agent
from abtestingstrategiesbackend.email import EmailVariant
from abtestingstrategiesbackend.environment import Environment
from abtestingstrategiesbackend.policy import EpsilonGreedyPolicy
from abtestingstrategiesbackend.rewards.reward_generator import (
    Probability,
    RewardGenerator,
)


def run_experiment():
    reward_probabilities = {
        EmailVariant(10): Probability(0.1),
        EmailVariant(20): Probability(0.9),
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
    for _ in range(1000):
        environment.process_email_sending()
    reward_over_sent_count = environment.statistics.get_reward_over_sent_count_data()
    return reward_over_sent_count
