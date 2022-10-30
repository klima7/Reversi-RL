from agents import RandomAgent
from gameplay import GuiGameplay, NoGuiGameplay

if __name__ == '__main__':
    agent1 = RandomAgent({}, False)
    agent2 = RandomAgent({}, False)

    gameplay = GuiGameplay(6, agent1, agent2)
    winner = gameplay.play()

    print(winner)
