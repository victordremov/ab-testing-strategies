import unittest
from datetime import timedelta, datetime

from abtestingstrategiesbackend.email import EmailVariant, Email
from abtestingstrategiesbackend.rewards.reward import Reward
from abtestingstrategiesbackend.rewards.reward_generator import RewardGenerator, Probability, UnknownEmailVariantError, \
    OutOfRangeException


class TestRewardGenerator(unittest.TestCase):
    @staticmethod
    def generate_reward_delay() -> timedelta:
        return timedelta(days=1)

    def test_output(self):

        reward_generator = RewardGenerator(
            reward_probabilities={
                EmailVariant(10): Probability(1.0),
                EmailVariant(20): Probability(0.0),
            },
            generate_reward_delay=self.generate_reward_delay,
        )
        with self.subTest(probability=1.0):
            email = Email(variant=EmailVariant(10), sending_datetime=datetime(2019, 1, 1))
            actual = reward_generator.generate(email)
            expected = Reward(value=1.0, cause=email, reward_datetime=datetime(2019, 1, 2))
            self.assertEqual(expected, actual)

        with self.subTest(probability=0.0):
            email = Email(variant=EmailVariant(20), sending_datetime=datetime(2019, 1, 1))
            actual = reward_generator.generate(email)
            self.assertIsNone(actual)

        email = Email(variant=EmailVariant(30), sending_datetime=datetime(2019, 1, 1))
        with self.assertRaises(UnknownEmailVariantError, msg='test raise when email variant is unknown'):
            reward_generator.generate(email)

    def test_probabilities_validation(self):
        with self.assertRaises(OutOfRangeException):
            RewardGenerator(
                reward_probabilities={
                    EmailVariant(10): Probability(1.01)
                },
                generate_reward_delay=self.generate_reward_delay
            )
        with self.assertRaises(OutOfRangeException):
            RewardGenerator(
                reward_probabilities={
                    EmailVariant(10): Probability(-0.01)
                },
                generate_reward_delay=self.generate_reward_delay
            )
