from .agent import Agent
from .expectimax import ExpectiMaxAgent
from .random import RandomAgent

ALL_AGENTS = {
    'expectimax': ExpectiMaxAgent,
    'random': RandomAgent
}
