from multiprocessing import freeze_support

from agents import RandomAgent
from gameplay import Gameplay

if __name__ == '__main__':
    freeze_support()

    agent1 = RandomAgent({}, False)
    agent2 = RandomAgent({}, False)

    gameplay = Gameplay(6, agent1, None, gui=True)
    winner = gameplay.play()

    print(winner)
