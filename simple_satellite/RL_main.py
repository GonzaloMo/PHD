from stable_baselines.common.env_checker import check_env

from simulation.RL_env import SimpleSat
from simulation.Simulation import SatelliteSim

Sim = SatelliteSim()
time_step =  Sim.PERIOD/Sim.CIRCUNFERENCE
env = SimpleSat(Sim, time_step)

# It will check your custom environment and output additional warnings if needed
check_env(env)
env.close()

from stable_baselines import PPO2 as agent
from stable_baselines.common.evaluation import evaluate_policy
#from stable_baselines.deepq.policies import MlpPolicy as policy
from stable_baselines.common.policies import MlpPolicy as policy
from stable_baselines.bench.monitor import Monitor

model = agent(policy, env, verbose=0)

env = Monitor(env, filename="RL/Log_RL")
# Train the agent for 10000 steps
model.learn(total_timesteps=10000)

mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
print(f"mean_reward:{mean_reward:.2f} +/- {std_reward:.2f}")
model.save("RL/Agent")