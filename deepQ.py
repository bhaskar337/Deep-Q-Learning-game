import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizers import Adam
from game_env import Game
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Agent:
    def __init__(self):

        #for experience replay
        self.memory = deque(maxlen=50000)
        self.gamma = 0.99    # discount rate

        self.epsilon = 0.1  # exploration rate
        self.epsilon_min = 0.0001
        self.epsilon_decay = 0.999

        self.learning_rate = 1e-6
        self.model = self._build_model()
        

    def _build_model(self):
        model = Sequential()
        model.add(Conv2D(32, (5,5), input_shape=(80,80,4), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (4,4), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(64, (3,3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dense(2, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    #for training
    #selects action based on game state with a epsilon probablity of a random action
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.choice([0,1])
        act_values = self.model.predict(state)
        return np.argmax(act_values[0]) 

    #for testing and demo
    def play(self, state):
        act_values = self.model.predict(state)
        return np.argmax(act_values[0]) 


    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    done = False
    batch_size = 32

    #total number of games to be played
    EPISODES = 15000
    #number of game states to observe before training
    OBSERVE = 10000

    env = Game()
    agent = Agent()

    #continue training
    # agent.load('training/ckpt_1000.h5')

    for e in range(EPISODES):
        env.reset()
        first = True
        while True:

            #perform no action for the first game state
            if first:
                action = 0
            else:
                action = agent.act(state)

            temp_state, reward, done, score = env.step(action)             
            next_state = np.reshape(np.stack(temp_state, axis=2), (1,80,80,4))

            if not first:
                agent.remember(state, action, reward, next_state, done)

            state = next_state

            if done:
                print("episode: {}/{}, score: {}".format(e, EPISODES, score))
                break
      
            first = False
            if OBSERVE != 0:
                OBSERVE -= 1

        if OBSERVE == 0:
            agent.replay(batch_size)

        if e % 10 == 0:
            agent.save("training/ckpt_" + str(e) + ".h5")

    agent.save("training/final.h5")

