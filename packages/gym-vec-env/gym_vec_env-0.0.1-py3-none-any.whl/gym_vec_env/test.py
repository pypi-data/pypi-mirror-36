import gym
from gym_vec_env import SubprocVecEnv

num_envs = 16
env_name = "CartPole-v0"


def make_env():
  def _thunk():
    env = gym.make(env_name)
    return env

  return _thunk


envs = [make_env() for i in range(num_envs)]
envs = SubprocVecEnv(envs)

env = gym.make(env_name)
