import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import click
import numpy as np

from agents import agents
from gameplay import GuiGameplay, NoGuiGameplay, Tournament


@click.command()
@click.argument('p1', type=click.Choice(list(agents.keys())), default='human')
@click.argument('p2', type=click.Choice(list(agents.keys())), default='human')
@click.option('-l1', is_flag=True, default=False, help='Enable learning for first player')
@click.option('-l2', is_flag=True, default=False, help='Enable learning for second player')
@click.option('-s', '--size', nargs=2, type=int, default=(8, 8), help='Size of the map')
@click.option('-n', '--number', type=int, default=1, help='Number of game repeats')
@click.option('--gui/--nogui', default=True, help='Whether graphical interface should be shown')
@click.option('-d', '--delay', type=float, default=0.05, help='Minimum delay between player moves in ms')
def reversi(p1, p2, l1, l2, size, number, gui, delay):
    if not gui and (p1 == 'human' or p2 == 'human'):
        print('Error: Human players are not allowed without GUI')
        return

    player1 = agents[p1](size, l1)
    player2 = agents[p2](size, l2)

    gameplay_class = GuiGameplay if gui else NoGuiGameplay
    gameplay = gameplay_class(size, delay)

    tournament = Tournament(gameplay, number, player1, player2)
    results = tournament.play()
    percent_results = np.array(results) / np.sum(results) * 100

    print('------------RESULTS------------')
    print(f'  Player1 ({p1}) wins: {results[0]} ({percent_results[0]:.1f}%)')
    print(f'  Player2 ({p2}) wins: {results[1]} ({percent_results[1]:.1f}%)')
    print(f'  Draws: {results[2]} ({percent_results[2]:.1f}%)')
    print('-------------------------------')


if __name__ == '__main__':
    reversi()
