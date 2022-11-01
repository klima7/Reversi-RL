from agents import RandomAgent
from gameplay import GuiGameplay, NoGuiGameplay, Tournament


# agent1 = RandomAgent({}, False)
# agent2 = RandomAgent({}, False)
#
# gameplay = GuiGameplay((4, 6), agent2, agent1, delay=0.1)
# winner = gameplay.play()
#
# print(winner)


agent1 = RandomAgent({}, False)
agent2 = RandomAgent({}, False)

gameplay = GuiGameplay((4, 6), delay=0.05)
tournament = Tournament(gameplay, None, agent1, agent2)
result = tournament.play()
print(result)
