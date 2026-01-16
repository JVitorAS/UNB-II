import gymnasium as gym
import numpy as np

class MK11Env(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, get_state_fn, get_hp_fn, do_action_fn):
        super().__init__()

        # Observação = [hp_player, hp_enemy]
        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(2,),
            dtype=np.float32
        )

        # Ações (12 ações básicas)
        self.action_space = gym.spaces.Discrete(12)

        self.get_state = get_state_fn
        self.get_hp = get_hp_fn
        self.do_action = do_action_fn

    def reset(self, seed=None, options=None):
        obs = self.get_observation()
        return obs, {}

    def step(self, action):
        # executa ação no jogo
        self.do_action(action)

        # nova observação
        obs = self.get_observation()

        # reward com base na diferença de HP
        reward = (self.last_enemy_hp - obs[1]) - (self.last_player_hp - obs[0])

        self.last_player_hp = obs[0]
        self.last_enemy_hp = obs[1]

        terminated = False  # fim da luta
        truncated = False

        return obs, reward, terminated, truncated, {}

    def get_observation(self):
        hp_player, hp_enemy = self.get_hp()
        self.last_player_hp = hp_player
        self.last_enemy_hp = hp_enemy
        return np.array([hp_player, hp_enemy], dtype=np.float32)
