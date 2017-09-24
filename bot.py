from deepQ import Agent
from game_env import Game
import numpy as np


def play():
    env = Game()
    agent = Agent()
    agent.load('training/ckpt_1310.h5')
    max_score = 0
    while True:
        env.reset()
        first = True
        while True:
            if first:
                action = 0
            else:
                action = agent.play(state)

            temp_state, reward, done, score = env.step(action)             
            next_state = np.reshape(np.stack(temp_state, axis=2), (1,80,80,4))

            state = next_state

            if done:
                if score > max_score:
                    max_score = score
                print("Score: {}  Max: {}".format(score, max_score))
                break
      
            first = False


play()