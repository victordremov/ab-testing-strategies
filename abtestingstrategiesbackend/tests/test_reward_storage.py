import unittest

from datetime import datetime, timedelta

from abtestingstrategiesbackend.email import Email, EmailVariant
from abtestingstrategiesbackend.rewards.reward import Reward
from abtestingstrategiesbackend.rewards.reward_storage import RewardStorage


class TestRewardStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.email = Email(
            variant=EmailVariant(0), sending_datetime=datetime(2019, 1, 1)
        )
        self.storage = RewardStorage()
        self.reward_first = Reward(
            value=1.0, cause=self.email, reward_datetime=datetime(2019, 1, 1)
        )
        self.reward_second = Reward(
            value=2.0, cause=self.email, reward_datetime=datetime(2019, 1, 2)
        )
        self.reward_third = Reward(
            value=3.0, cause=self.email, reward_datetime=datetime(2019, 1, 3)
        )

    def test_output_order(self):
        for reward in [self.reward_first, self.reward_second, self.reward_third]:
            self.storage.add(reward)
        actual = self.storage.get_all_until(datetime(2019, 1, 3))
        expected = [self.reward_first, self.reward_second, self.reward_third]
        self.assertListEqual(expected, actual)

        for reward in [self.reward_third, self.reward_second, self.reward_first]:
            self.storage.add(reward)
        actual = self.storage.get_all_until(datetime(2019, 1, 3))
        expected = [self.reward_first, self.reward_second, self.reward_third]
        self.assertListEqual(expected, actual)

    def test_get_all_until(self):
        reward = self.reward_first

        with self.subTest("test event after max_reward_datetime not returned"):
            self.storage.add(reward)
            before_reward = reward.reward_datetime - timedelta(microseconds=1)
            actual = self.storage.get_all_until(before_reward)
            self.assertListEqual([], actual)

        with self.subTest(
            "test event with datetime equal to max_reward_datetime returned"
        ):
            exactly_reward = reward.reward_datetime
            actual = self.storage.get_all_until(exactly_reward)
            expected = [reward]
            self.assertListEqual(expected, actual)

        with self.subTest("test event before max_reward_datetime returned"):
            self.storage.add(reward)
            after_reward = reward.reward_datetime + timedelta(microseconds=1)
            actual = self.storage.get_all_until(after_reward)
            expected = [reward]
            self.assertListEqual(expected, actual)

    def test_output_for_empty_storage(self):
        actual = self.storage.get_all_until(datetime(2019, 1, 3))
        expected = []
        self.assertListEqual([], actual)

    def test_item_removing(self):
        self.storage.add(self.reward_first)
        self.storage.add(self.reward_second)

        between_first_and_second = datetime(2019, 1, 1, 12)
        assert (
            self.reward_first.reward_datetime
            < between_first_and_second
            < self.reward_second.reward_datetime
        )
        with self.subTest("test get_all_until removes retreaved items from storage"):
            rewards_retreaved = self.storage.get_all_until(between_first_and_second)
            self.assertListEqual([self.reward_first], rewards_retreaved)
            actual = self.storage.get_all_until(between_first_and_second)
            expected = []
            self.assertListEqual(expected, actual)

        with self.subTest("test not retreaved items not "):
            after_second = datetime(2099, 1, 1)
            actual = self.storage.get_all_until(after_second)
            self.assertListEqual([self.reward_second], actual)
