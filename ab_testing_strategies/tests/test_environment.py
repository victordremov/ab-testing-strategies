import unittest
from datetime import timedelta, datetime

from ab_testing_strategies.agent import Agent
from ab_testing_strategies.email import EmailVariant
from ab_testing_strategies.environment import Environment
from ab_testing_strategies.policy import EpsilonGreedyPolicy
from ab_testing_strategies.rewards.reward_generator import Probability, RewardGenerator


class MyTestCase(unittest.TestCase):
    def test_process_email_sending(self):
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
        reward_over_sent_count = (
            environment.statistics.get_reward_over_sent_count_data()
        )
        email_variant_probabilities = environment.statistics.get_probabilities_data()