from queue import PriorityQueue
from typing import List, Tuple

from datetime import datetime

from abtestingstrategiesbackend.rewards.reward import Reward


class RewardStorage:
    def __init__(self):
        self._priority_queue: PriorityQueue = PriorityQueue()

    def get_all_until(self, max_reward_datetime: datetime) -> List[Reward]:
        rewards = []
        reward_datetime = max_reward_datetime
        while not self._priority_queue.empty() and reward_datetime <= max_reward_datetime:
            item: Tuple[datetime, Reward] = self._priority_queue.get_nowait()
            reward_datetime, reward = item
            if reward_datetime <= max_reward_datetime:
                rewards.append(reward)
            else:
                self._priority_queue.put_nowait(item)
        return rewards

    def add(self, reward: Reward) -> None:
        priority = reward.reward_datetime
        self._priority_queue.put_nowait((priority, reward))