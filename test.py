from game_state import GameState

gs1 = GameState((3, 3))
gs2 = GameState((3, 3))

s = set()
s.add(gs1)

print(gs2 in s)
