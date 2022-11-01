# to hide pygame welcome message
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

# normal imports imports
import click
from agents import agents

from gameplay import GuiGameplay, NoGuiGameplay


@click.command()
@click.option('-p1', type=click.Choice([*agents.keys(), 'human']), default='human', help='Type of white player')
@click.option('-p2', type=click.Choice([*agents.keys(), 'human']), default='human', help='Type of black player')
@click.option('-l1', is_flag=True, default=False, help='Enable learning for white player')
@click.option('-l2', is_flag=True, default=False, help='Enable learning for black player')
@click.option('-s', '--size', nargs=2, type=int, default=(8, 8), help='Size of the map')
@click.option('-n', '--number', type=int, default=1, help='Number of game repeats')
@click.option('--gui/--no-gui', default=True, help='Whether graphical interface should be shown')
@click.option('-d', '--delay', type=float, default=0.1, help='Minimum delay between player moves in ms')
def reversi(p1, p2, l1, l2, size, number, gui, delay):
    print(p1, p2, l1, l2, size, number, gui, delay)


if __name__ == '__main__':
    reversi()
