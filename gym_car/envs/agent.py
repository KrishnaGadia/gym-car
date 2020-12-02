import gym

env = gym.make('gym_car:car-v0')
env.reset()
for step in range(1000):
    env.render()
    action=env.action_space.sample()
    observation, reward, done, info = env.step(action) # take a random action
    print(action)
    if done:
       print(" Done in "+str(step))
       break
#env.close()