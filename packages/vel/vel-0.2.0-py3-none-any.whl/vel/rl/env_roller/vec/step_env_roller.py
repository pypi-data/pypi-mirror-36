import torch
import numpy as np

from vel.rl.api.base import EnvRollerBase, EnvRollerFactory


class StepEnvRoller(EnvRollerBase):
    """
    Class calculating env rollouts.
    Idea behind this class is to store as much as we can as pytorch tensors to minimize tensor copying.
    """

    def __init__(self, environment, device, number_of_steps, discount_factor, gae_lambda=1.0):
        self._environment = environment
        self.device = device
        self.number_of_steps = number_of_steps
        self.discount_factor = discount_factor
        self.gae_lambda = gae_lambda

        # Initial observation
        self.observation = self._to_tensor(self.environment.reset())
        self.dones = torch.tensor([False for _ in range(self.observation.shape[0])], device=self.device)

        self.batch_observation_shape = (
            (self.observation.shape[0]*self.number_of_steps,) + self.environment.observation_space.shape
        )

        self.action_observation_shape = (
            (self.observation.shape[0]*self.number_of_steps,) + self.environment.action_space.shape
        )

    @property
    def environment(self):
        """ Return environment of this env roller """
        return self._environment

    def _to_tensor(self, numpy_array):
        """ Convert numpy array to a tensor """
        return torch.from_numpy(numpy_array).to(self.device)

    @torch.no_grad()
    def rollout(self, batch_info, model):
        """ Calculate env rollout """
        observation_accumulator = []  # Device tensors
        action_accumulator = []  # Device tensors
        value_accumulator = []  # Device tensors
        dones_accumulator = []  # Device tensors
        rewards_accumulator = []  # Device tensors
        episode_information = []  # Python objects
        logprob_accumulator = []  # Device tensors

        for step_idx in range(self.number_of_steps):
            step = model.step(self.observation)
            actions, values, logprob = step['actions'], step['values'], step['logprob']

            observation_accumulator.append(self.observation)
            action_accumulator.append(actions)
            value_accumulator.append(values)
            dones_accumulator.append(self.dones)
            logprob_accumulator.append(logprob)

            actions_numpy = actions.detach().cpu().numpy()
            new_obs, new_rewards, new_dones, new_infos = self.environment.step(actions_numpy)

            # Done is flagged true when the episode has ended AND the frame we see is already a first frame from the
            # Next episode
            self.dones = self._to_tensor(new_dones.astype(np.uint8))
            self.observation = self._to_tensor(new_obs[:])

            rewards_accumulator.append(self._to_tensor(new_rewards.astype(np.float32)))

            for info in new_infos:
                maybe_episode_info = info.get('episode')

                if maybe_episode_info:
                    episode_information.append(maybe_episode_info)

        last_values = model.value(self.observation)
        dones_accumulator.append(self.dones)

        observation_buffer = torch.stack(observation_accumulator)
        rewards_buffer = torch.stack(rewards_accumulator)
        # There may be different types of actions
        actions_buffer = torch.stack(action_accumulator)
        values_buffer = torch.stack(value_accumulator)
        dones_buffer = torch.stack(dones_accumulator)
        logprob_buffer = torch.stack(logprob_accumulator)

        masks_buffer = dones_buffer[:-1, :]
        dones_buffer = dones_buffer[1:, :]

        # Generalized Advantage Estimation
        # https://arxiv.org/abs/1506.02438
        advantages = self.discount_bootstrap_gae(
            rewards_buffer, dones_buffer, values_buffer, last_values,
            self.discount_factor, self.gae_lambda
        )

        returns = advantages + values_buffer

        # Flatten the rollout
        advantages = advantages.flatten()
        returns = returns.flatten()
        values = values_buffer.flatten()
        masks = masks_buffer.flatten()
        dones = dones_buffer.flatten()
        logprobs = logprob_buffer.flatten()

        # Reshape into final batch size
        return {
            'size': advantages.size(0),
            'observations': observation_buffer.reshape(self.batch_observation_shape),
            'returns': returns,
            'masks': masks,
            'dones': dones,
            'actions': actions_buffer.reshape(self.action_observation_shape),
            'values': values,
            'advantages': advantages,
            'episode_information': episode_information,
            'logprobs': logprobs
        }

    def discount_bootstrap(self, rewards_buffer, dones_buffer, last_values_buffer, discount_factor):
        """ Calculate state values bootstrapping off the following state values """
        true_value_buffer = torch.zeros_like(rewards_buffer)
        dones_buffer = dones_buffer.to(dtype=torch.float32)

        # discount/bootstrap off value fn
        current_value = last_values_buffer

        for i in reversed(range(self.number_of_steps)):
            current_value = rewards_buffer[i] + discount_factor * current_value * (1.0 - dones_buffer[i])
            true_value_buffer[i] = current_value

        return true_value_buffer

    def discount_bootstrap_gae(self, rewards_buffer, dones_buffer, values_buffer, last_values_buffer,
                               discount_factor, gae_lambda):
        """ Calculate state values bootstrapping off the following state values - Generalized Advantage Estimation """
        advantage_buffer = torch.zeros_like(rewards_buffer)
        dones_buffer = dones_buffer.to(dtype=torch.float32)

        # Accmulate sums
        sum_accumulator = 0

        for i in reversed(range(self.number_of_steps)):
            if i == self.number_of_steps - 1:
                next_value = last_values_buffer
            else:
                next_value = values_buffer[i+1]

            bellman_delta = (
                rewards_buffer[i] + discount_factor * next_value * (1.0 - dones_buffer[i]) - values_buffer[i]
            )

            advantage_buffer[i] = sum_accumulator = (
                bellman_delta + discount_factor * gae_lambda * sum_accumulator * (1.0 - dones_buffer[i])
            )

        return advantage_buffer


class StepEnvRollerFactory(EnvRollerFactory):
    """ Factory for the StepEnvRoller """
    def __init__(self, gae_lambda=1.0):
        self.gae_lambda = gae_lambda

    def instantiate(self, environment, device, settings):
        return StepEnvRoller(
            environment=environment,
            device=device,
            number_of_steps=settings.number_of_steps,
            discount_factor=settings.discount_factor,
            gae_lambda=self.gae_lambda
        )


def create(gae_lambda=1.0):
    return StepEnvRollerFactory(gae_lambda=gae_lambda)

