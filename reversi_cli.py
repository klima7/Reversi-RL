import click


PLAYER_CHOICES = ['user', 'random', 'simple', 'minimax']


@click.command()
@click.option('-pw', '--player-white', type=click.Choice(PLAYER_CHOICES), required=True, help='Type of white player')
@click.option('-pw', '--player-black', type=click.Choice(PLAYER_CHOICES), required=True, help='Type of black player')
@click.option('-lw', '--learn-white', is_flag=True, default=False, help='Enable learning for white player')
@click.option('-lb', '--learn-black', is_flag=True, default=False, help='Enable learning for black player')
@click.option('-s', '--size', type=int, default=8, help='Size of the map')
@click.option('-n', '--number', type=int, default=1, help='Number of game repeats')
@click.option('--gui/--no-gui', default=False, help='Whether graphical interface should be shown')
@click.option('-d', '--delay', type=int, default=300, help='Minimum delay between player moves in ms')
def reversi_cli():
    pass


if __name__ == '__main__':
    reversi_cli()
