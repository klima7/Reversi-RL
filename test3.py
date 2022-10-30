from agents import RandomAgent
from gameplay_gui import GameplayGui

agent1 = RandomAgent({}, False)
agent2 = RandomAgent({}, False)

gameplay = GameplayGui(4, agent1, agent2)
winner = gameplay.play()

print(winner)
