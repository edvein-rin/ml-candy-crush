import numpy as np
import matplotlib.pyplot as plt

def plot_cumulative_rewards(models, rewards):
    # Plotting the cumulative rewards
    for model in models:
        cumulative_rewards = np.cumsum(rewards[model])
        plt.plot(cumulative_rewards, label=model)
    plt.legend()
    plt.title('Cumulative Reward')
    plt.xlabel('Steps')
    plt.ylabel('Reward')
    plt.grid(True)
    plt.show()


def plot_total_rewards(models, rewards):
    # Plotting the total rewards
    total_rewards = {model: sum(rewards[model]) for model in models}
    colors = ['C0' if model == 'DQN' else 'C2' if model == 'Greedy' else 'C1' for model in total_rewards.keys()]
    bars = plt.bar(total_rewards.keys(), total_rewards.values(), color=colors)
    plt.xlabel('Models')
    plt.ylabel('Total Reward')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval, f'Total Reward: {int(yval)}', va='bottom')  # va: vertical alignment

    plt.show()