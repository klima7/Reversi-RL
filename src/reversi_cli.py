import click

from gameplay import GuiGameplay, NoGuiGameplay


PLAYER_CHOICES = ['user', 'random', 'simple', 'minimax']


@click.command()
@click.option('-p1', type=click.Choice(PLAYER_CHOICES), required=True, help='Type of white player')
@click.option('-p2', type=click.Choice(PLAYER_CHOICES), required=True, help='Type of black player')
@click.option('-l1', is_flag=True, default=False, help='Enable learning for white player')
@click.option('-l2', is_flag=True, default=False, help='Enable learning for black player')
@click.option('-s', '--size', type=int, default=8, help='Size of the map')
@click.option('-n', '--number', type=int, default=1, help='Number of game repeats')
@click.option('--gui/--no-gui', default=False, help='Whether graphical interface should be shown')
@click.option('-d', '--delay', type=int, default=300, help='Minimum delay between player moves in ms')
def reversi_cli():
    pass


def play_batch(gameplay, player1, player2, number):
    players = [player1, player2]

    for gameplay_no in range(number):
        gameplay = gameplay_class()

if __name__ == '__main__':
    reversi_cli()
