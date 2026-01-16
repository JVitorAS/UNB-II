from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
import os


class PPOAgent:
    def __init__(
        self,
        env,
        model_path="models/ppo_mk",
        learning_rate=3e-4,
        gamma=0.99,
        n_steps=1024,
        batch_size=256
    ):
        self.env = DummyVecEnv([lambda: env])
        self.model_path = model_path

        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        if os.path.exists(model_path + ".zip"):
            self.model = PPO.load(model_path, env=self.env)
            print("[PPO] Modelo carregado.")
        else:
            self.model = PPO(
                policy="MlpPolicy",
                env=self.env,
                learning_rate=learning_rate,
                gamma=gamma,
                n_steps=n_steps,
                batch_size=batch_size,
                verbose=1
            )
            print("[PPO] Novo modelo criado.")

    # -------------------------
    # TREINO
    # -------------------------
    def treinar(self, timesteps=100_000, salvar_cada=50_000):
        checkpoint = CheckpointCallback(
            save_freq=salvar_cada,
            save_path=os.path.dirname(self.model_path),
            name_prefix="ppo_checkpoint"
        )

        self.model.learn(
            total_timesteps=timesteps,
            callback=checkpoint
        )

        self.model.save(self.model_path)
        print("[PPO] Treino finalizado e modelo salvo.")

    # -------------------------
    # INFERÊNCIA (FRAME-LEVEL)
    # -------------------------
    def decidir_acao(self, obs):
        """
        Recebe observação (np.array)
        Retorna ação (int)
        """
        action, _ = self.model.predict(obs, deterministic=False)
        return int(action)

    # -------------------------
    # SALVAR / CARREGAR
    # -------------------------
    def salvar(self):
        self.model.save(self.model_path)

    def carregar(self):
        self.model = PPO.load(self.model_path, env=self.env)
