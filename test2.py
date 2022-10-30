from agents import RandomAgent
from gameplay import Gameplay

agent1 = RandomAgent({}, False)
agent2 = RandomAgent({}, False)

gameplay = Gameplay(8, agent1, None)
moves = gameplay.game_state.get_moves()
print(moves)
