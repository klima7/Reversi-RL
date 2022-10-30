from agents import RandomAgent
from gameplay import Gameplay

agent1 = RandomAgent({}, False)
agent2 = RandomAgent({}, False)

gameplay = Gameplay(4, agent1, agent2)
winner = gameplay.play()

gameplay.game_state.plot()

print(winner)
