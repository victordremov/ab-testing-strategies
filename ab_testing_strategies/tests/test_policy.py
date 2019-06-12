import unittest
import unittest.mock

from datetime import datetime

from ab_testing_strategies.email import EmailVariant, Email
from ab_testing_strategies.policy import EpsilonGreedyPolicy, EmailVariantStatistics
from ab_testing_strategies.rewards.reward import Reward
from ab_testing_strategies.rewards.reward_generator import Probability


class TestPolicy(unittest.TestCase):
    def test_choose_variant(self):
        policy = EpsilonGreedyPolicy(
            epsilon=Probability(0.0),
            email_variants=[EmailVariant(10), EmailVariant(20), EmailVariant(30)],
        )
        for _ in range(2):
            policy._increment_n_attempts(EmailVariant(10))
            policy._increment_n_attempts(EmailVariant(20))
            policy._increment_n_attempts(EmailVariant(30))

        for _ in range(2):
            policy._increment_n_succeses(EmailVariant(10))
        policy._increment_n_succeses(EmailVariant(20))
        actual = policy.choose_email_variant()
        expected = EmailVariant(10)
        self.assertEqual(expected, actual)

    def test_update(self):
        policy = EpsilonGreedyPolicy(
            epsilon=Probability(0.0),
            email_variants=[EmailVariant(10), EmailVariant(20)],
        )
        with self.subTest("assert n_attempts_incremented"):
            policy.update_statistics(
                event=Email(
                    variant=EmailVariant(10), sending_datetime=datetime(2019, 1, 1)
                )
            )
            self.assertDictEqual(
                {
                    EmailVariant(10): EmailVariantStatistics(
                        n_attempts=1, n_successes=0
                    ),
                    EmailVariant(20): EmailVariantStatistics(
                        n_attempts=0, n_successes=0
                    ),
                },
                policy.email_variants_statistics,
            )
        with self.subTest("assert n_attempts_incremented"):
            policy.update_statistics(
                event=Reward(
                    value=1,
                    reward_datetime=datetime(2019, 1, 1),
                    cause=Email(
                        variant=EmailVariant(10), sending_datetime=datetime(2019, 1, 1)
                    ),
                )
            )
            self.assertDictEqual(
                {
                    EmailVariant(10): EmailVariantStatistics(
                        n_attempts=1, n_successes=1
                    ),
                    EmailVariant(20): EmailVariantStatistics(
                        n_attempts=0, n_successes=0
                    ),
                },
                policy.email_variants_statistics,
            )
