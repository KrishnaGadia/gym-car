from gym.envs.registration import register

register(
    id='car-v0',
    entry_point='gym_car.envs:CarEnv',
)
