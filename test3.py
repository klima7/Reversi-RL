from agents import RandomAgent
from gameplay_gui import GameplayGui

agent1 = RandomAgent({}, False)
agent2 = RandomAgent({}, False)

gameplay = GameplayGui(4, agent1, None)
winner = gameplay.play()

print(winner)
