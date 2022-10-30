from agents import RandomAgent
from gameplay import GuiGameplay

if __name__ == '__main__':
    agent1 = RandomAgent({}, False)
    agent2 = RandomAgent({}, False)

    gameplay = GuiGameplay(6, agent1, None)
    winner = gameplay.play()

    print(winner)
