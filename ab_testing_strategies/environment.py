from datetime import datetime, timedelta

from ab_testing_strategies.agent import Agent
from ab_testing_strategies.email import Email
from ab_testing_strategies.rewards.reward_generator import RewardGenerator
from ab_testing_strategies.rewards.reward_storage import RewardStorage


class Environment:
    def __init__(self, agent: Agent, reward_generator: RewardGenerator):
        self.agent = agent
        self.reward_generator = reward_generator
        self.reward_storage = RewardStorage()
        self.time = datetime.now()
        self.interval_to_send_single_mail = timedelta(minutes=1)

    def process_email_sending(self) -> None:
        email = self.agent.fill_email_variant(Email(sending_datetime=self.time))
        reward = self.reward_generator.generate(email)
        if reward is not None:
            self.reward_storage.add(reward)
        self.increment_time()
        rewards = self.collect_rewards()
        self.agent.process_rewards(rewards)

    def collect_rewards(self):
        return self.reward_storage.get_all_until(self.time)

    def increment_time(self):
        self.time += self.interval_to_send_single_mail
