from agents import RandomAgent
from gameplay import GuiGameplay, NoGuiGameplay, Tournament


# agent1 = RandomAgent({}, False)
# agent2 = RandomAgent({}, False)
#
# gameplay = GuiGameplay((4, 6), agent2, agent1, delay=0.1)
# winner = gameplay.play()
#
# print(winner)

size = (4, 6)

agent1 = RandomAgent(size, False)
agent2 = RandomAgent(size, False)

gameplay = NoGuiGameplay(size, delay=0.05)
tournament = Tournament(gameplay, 100, agent1, agent2)
result = tournament.play()
print(result)
