from agents import agents, RandomAgent
from gameplay import GuiGameplay, NoGuiGameplay

if __name__ == '__main__':
    agent1 = RandomAgent({}, False)
    agent2 = RandomAgent({}, False)

    gameplay = GuiGameplay((4, 6), None, None, delay=0.1)
    winner = gameplay.play()

    print(winner)
