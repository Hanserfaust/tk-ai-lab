import gym

from gym.spaces import Discrete


class WildernessEnv(gym.Env):
    """
    WildernessEnv

    Below taken from gym.Env

    The main OpenAI Gym class. It encapsulates an environment with
    arbitrary behind-the-scenes dynamics. An environment can be
    partially or fully observed.

    The main API methods that users of this class need to know are:

        step
        reset
        render
        close
        seed

    When implementing an environment, override the following methods
    in your subclass:

        _step
        _reset
        _render
        _close
        _seed

    And set the following attributes:

        action_space: The Space object corresponding to valid actions
        observation_space: The Space object corresponding to valid observations
        reward_range: A tuple corresponding to the min and max possible rewards

    Note: a default reward range set to [-inf,+inf] already exists. Set it if you want a narrower range.

    The methods are accessed publicly as "step", "reset", etc.. The
    non-underscored versions are wrapper methods to which we may add
    functionality over time.
    """

    def __init__(self):

        # There is 4 actions atm: w,a,s,d for movement
        action_space = Discrete(4)

        #
        observation_space = self.reset()
        reward_range = None

    def _close(self):
        super()._close()

    def _seed(self, seed=None):
        return super()._seed(seed)

    def _step(self, action):
        pass

    def _render(self, mode='human', close=False):
        super()._render(mode, close)

    def _reset(self):
        pass
