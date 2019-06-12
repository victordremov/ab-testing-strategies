from typing import Union, List

from abtestingstrategiesbackend.email import Email
from abtestingstrategiesbackend.policy import Policy
from abtestingstrategiesbackend.rewards.reward import Reward


class Agent:
    def __init__(self, policy: Policy) -> None:
        self._policy = policy

    def update_policy_statistics(self, event: Union[Email, Reward]) -> None:
        self._policy.update_statistics(event)

    def fill_email_variant(self, email: Email) -> Email:
        filled_email = Email(
            sending_datetime=email.sending_datetime,
            variant=self._policy.choose_email_variant(),
        )
        self.update_policy_statistics(filled_email)
        return filled_email

    def process_rewards(self, rewards: List[Reward]) -> None:
        for reward in rewards:
            self.update_policy_statistics(reward)
