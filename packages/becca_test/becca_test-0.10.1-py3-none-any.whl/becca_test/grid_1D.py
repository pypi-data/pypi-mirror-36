"""
One-dimensional grid task.

This task tests a brain's ability to choose an appropriate action.
It is straightforward. Reward and punishment is clear and immediate.
There is only one reward state and it can be reached in a single
step.

Usage
To run this world standalone from the command line

    python333 -m grid_1D

"""
import numpy as np

import becca.brain as becca_brain
from becca.base_world import World as BaseWorld


class World(BaseWorld):
    """
    One-dimensional grid world.

    In this task, the brain steps forward and backward along
    a nine-position line. The fourth position is rewarded and
    the ninth position is punished. There is also a slight
    punishment for effort expended in taking actions.
    Occasionally the brain will get
    involuntarily bumped to a random position on the line.
    This is intended to be a simple-as-possible
    task for troubleshooting Becca.
    Optimal performance is a reward of about 90 per time step.

    Most of this world's attributes are defined in base_world.py.
    The few that aren't are defined below.
    """
    def __init__(self, lifespan=None):
        """
        Initialize the world.

        Parameters
        ----------
        lifespan : int
            The number of time steps to continue the world.
        """
        BaseWorld.__init__(self, lifespan)
        self.name = 'grid_1D'
        print("Entering", self.name)

        self.n_sensors = 9
        self.num_positions = self.n_sensors
        self.n_actions = 8
        self.action = np.zeros(self.n_actions)
        self.energy = 0.
        # energy_cost : float
        #     The punishment per position step taken.
        self.energy_cost = 1. / 100.
        # world_state : float
        #     The actual position of the agent in the world.
        #     This can be fractional.
        self.world_state = 0
        # simple_state : int
        #     The nearest integer position of the agent in the world.
        self.simple_state = 0
        # jump_fraction : float
        #     The fraction of time steps on which the agent jumps to
        #     a random position.
        self.jump_fraction = 0.1

        self.visualize_interval = 1e6

    def step(self, action):
        """
        Advance the world one time step.

        Parameters
        ----------
        action : array of floats
            The set of action commands to execute.

        Returns
        -------
        reward : float
            The amount of reward or punishment given by the world.
        sensors : array of floats
            The values of each of the sensors.
        """
        self.action = action
        self.action = np.round(self.action)
        self.timestep += 1

        # Find the step size as combinations of the action commands
        #     action[i]     result
        #            0      1 step to the right
        #            1      2 steps to the right
        #            2      3 steps to the right
        #            3      4 steps to the right
        #            4      1 step to the left
        #            5      2 steps to the left
        #            6      3 steps to the left
        #            7      4 steps to the left
        step_size = (self.action[0] +
                     self.action[1] * 2 +
                     self.action[2] * 3 +
                     self.action[3] * 4 -
                     self.action[4] -
                     self.action[5] * 2 -
                     self.action[6] * 3 -
                     self.action[7] * 4)
        # Action cost is an approximation of metabolic energy.
        # Action cost is proportional to the number of steps taken.
        self.energy = (self.action[0] +
                       self.action[1] * 2 +
                       self.action[2] * 3 +
                       self.action[3] * 4 +
                       self.action[4] +
                       self.action[5] * 2 +
                       self.action[6] * 3 +
                       self.action[7] * 4)

        self.world_state += step_size

        # At random intervals, jump to a random position in the world.
        if np.random.random_sample() < self.jump_fraction:
            self.world_state = self.num_positions * np.random.random_sample()

        # Ensure that the world state falls between 0 and 9.
        self.world_state -= self.num_positions * np.floor_divide(
            self.world_state, self.num_positions)
        self.simple_state = int(np.floor(self.world_state))
        if self.simple_state == 9:
            self.simple_state = 0

        sensors = self.sense()
        reward = self.assign_reward()
        return sensors, reward

    def sense(self):
        """
        Represent the presence or absence of the current position in the bin.

        Returns
        -------
        sensors : array of float
            The current sensor values.
        """
        sensors = np.zeros(self.n_sensors)
        sensors[self.simple_state] = 1
        return sensors

    def assign_reward(self):
        """
        Calculate the total reward corresponding to the current state

        Returns
        -------
        reward : float
            The reward associated the set of input sensors.
        """
        reward = 0.
        if int(self.world_state) == 3:
            reward += 1.
        if int(self.world_state) == 8:
            reward -= 1.
        # Punish actions just a little
        reward -= self.energy * self.energy_cost
        reward = np.maximum(reward, -1.)

        return reward

    def visualize(self):
        """
        Show what's going on in the world.
        """
        state_image = ['.'] * (self.n_sensors + self.n_actions + 2)
        state_image[int(self.world_state)] = 'O'
        state_image[self.n_sensors:self.n_sensors + 2] = '||'
        action_index = np.where(self.action > 0.1)[0]
        if action_index.size > 0:
            for i in range(action_index.size):
                state_image[self.n_sensors + 2 + action_index[i]] = 'x'
        print(''.join(state_image))


if __name__ == "__main__":
    becca_brain.run(World())
