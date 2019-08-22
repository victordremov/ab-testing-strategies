from sys import stderr

from numpy import mean
from tqdm import tqdm

from abtestingstrategiesbackend.run import run_thompson_sampling_experiment

if __name__ == "__main__":
    n_retries = 1000
    results = []
    n_emails = 10000
    for prior_alpha, prior_beta in [(1, 1), (11, 101), (12, 101), (51, 501), (56, 501), (101, 1001), (111, 1001)]:
        for i in tqdm(range(n_retries)):
            t = run_thompson_sampling_experiment(
                n_emails=n_emails,
                probability_a=0.10,
                probability_b=0.12,
                prior_alpha=100,
                prior_beta=1000,
            )
            results.append(t["cumulative_reward"].iloc[-1])
        print(f"Prior: {prior_alpha, prior_beta}. Average conversion rate: {mean(results) / n_emails * 100: .2f}%", file=stderr)
