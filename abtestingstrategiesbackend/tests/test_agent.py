import unittest

from datetime import datetime
from unittest.mock import MagicMock

from abtestingstrategiesbackend.agent import Agent
from abtestingstrategiesbackend.email import EmailVariant, Email
from abtestingstrategiesbackend.policy import EpsilonGreedyPolicy
from abtestingstrategiesbackend.rewards.reward_generator import Probability


class TestAgent(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = Agent(policy=EpsilonGreedyPolicy(epsilon=Probability(0.5), email_variants=[EmailVariant(10)]))
        self.email = Email(sending_datetime=(datetime(2019, 1, 1)), variant=None)
    def test_fill_email_variant(self):


        filled_actual = self.agent.fill_email_variant(self.email)
        filled_expected = Email(sending_datetime=self.email.sending_datetime, variant=EmailVariant(10))
        self.assertEqual(filled_expected, filled_actual)

    def test_update_policy_statistics(self):
        mocked_update_statistics = MagicMock()
        self.agent._policy.update_statistics = mocked_update_statistics
        email = self.agent.fill_email_variant(self.email)
        mocked_update_statistics.assert_called_once_with(email)

    def test_fill_email_variant_triggers_update_policy_statistics(self):
        mocked_update_statistics = MagicMock()
        self.agent._policy.update_statistics = mocked_update_statistics
        email = self.agent.fill_email_variant(self.email)
        mocked_update_statistics.assert_called_once_with(email)
