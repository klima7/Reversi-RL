from typing import Optional, Dict

from agents import Agent


"""
Output:
{
- winner: bool
- p1_discs, p2_discs: int
- knowledge1, knowledge2: dict
}
"""


class Othello:

    def __init__(
            self,
            gui: bool,
            size: int,
            speed: int,
            agent1: Optional[Agent],
            agent2: Optional[Agent],
            knowledge1: Optional[Dict],
            knowledge2: Optional[Dict],
            learn1: bool,
            learn2: bool,
    ):

        def play():
            pass
