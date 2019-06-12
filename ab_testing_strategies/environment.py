from datetime import datetime, timedelta

from typing import Optional, List, Dict

from dataclasses import dataclass, field
import pandas as pd

from ab_testing_strategies.agent import Agent
from ab_testing_strategies.email import Email, EmailVariant
from ab_testing_strategies.rewards.reward import Reward
from ab_testing_strategies.rewards.reward_generator import RewardGenerator, Probability
from ab_testing_strategies.rewards.reward_storage import RewardStorage


@dataclass
class EnvironmentStatistics:
    email_variants: List[EmailVariant]
    datetime: List[datetime]
    probabilities: Dict[EmailVariant, List[float]]
    cumulative_sent_emails_count: List[int]
    cumulative_reward: List[int]

    def update(
        self,
        new_rewards: List[Reward],
        datetime_: datetime,
        current_probabilities: Dict[EmailVariant, float],
    ) -> None:
        self.datetime.append(datetime_)
        for email_variant, probability in current_probabilities.items():
            self.probabilities[email_variant].append(probability)
        self.cumulative_reward.append(
            self.cumulative_reward[-1] + sum(r.value for r in new_rewards)
        )
        self.cumulative_sent_emails_count.append(
            self.cumulative_sent_emails_count[-1] + 1
        )

    def get_reward_over_sent_count_data(self):
        total_cumulative_counts = pd.DataFrame(
            {
                "cumulative_sent_emails_count": self.cumulative_sent_emails_count,
                "cumulative_reward": self.cumulative_reward,
                "datetime": self.datetime,
            }
        )
        return total_cumulative_counts

    def get_probabilities_data(self):
        probabilities = pd.DataFrame(self.probabilities)
        probabilities["datetime"] = self.datetime
        return probabilities


class Environment:
    def __init__(
        self,
        agent: Agent,
        reward_generator: RewardGenerator,
        start_datetime: Optional[datetime] = None,
    ) -> None:
        self.agent = agent
        self.reward_generator = reward_generator
        self.reward_storage = RewardStorage()
        if start_datetime is None:
            start_datetime = datetime.now()
        self.time = start_datetime
        self.interval_to_send_single_mail = timedelta(minutes=1)

        email_variants = list(reward_generator._reward_probabilities.keys())

        self.statistics = EnvironmentStatistics(
            email_variants=email_variants,
            datetime=[self.time],
            probabilities={
                variant: [len(email_variants)] for variant in email_variants
            },
            cumulative_sent_emails_count=[0],
            cumulative_reward=[0],
        )

    def process_email_sending(self) -> None:
        email = self.agent.fill_email_variant(Email(sending_datetime=self.time))
        reward = self.reward_generator.generate(email)
        if reward is not None:
            self.reward_storage.add(reward)
        self.increment_time()
        rewards = self.collect_rewards()
        self.agent.process_rewards(rewards)
        self.statistics.update(
            rewards, self.time, self.agent._policy.get_current_probabilities()
        )

    def collect_rewards(self):
        return self.reward_storage.get_all_until(self.time)

    def increment_time(self):
        self.time += self.interval_to_send_single_mail
