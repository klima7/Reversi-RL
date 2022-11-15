# Reversi
<img src="https://github.com/klima7/Reversi/blob/main/screenshot.png" width="200" />

## Overview
Othello game prepared for reinforcement learning with following agents implemented:
- Value Iteration
- MCTS
- SARSA
- SARSA-Lambda
- Expected SARSA
- Q-Learning
- Double Q-Learning
- Value Function Approximation
- Random

## Usage
Inside src directory: `python reversi.py --help`:
```
Usage: reversi.py [OPTIONS] [[human|random|value_iter|mcts|sarsa|exp_sarsa|sar
                  sa_lambda|q_learning|dq_learning|value_approx]] [[human|rand
                  om|value_iter|mcts|sarsa|exp_sarsa|sarsa_lambda|q_learning|d
                  q_learning|value_approx]]

  Runs Reversi game of given size, given number of times, with selected
  players, which are learning or not, with or without GUI and returns wins
  count

Options:
  -l1                    Enable learning for first player
  -l2                    Enable learning for second player
  -s, --size INTEGER...  Size of the map
  -n, --number INTEGER   Number of game repeats
  -d, --delay FLOAT      Minimum delay between player moves in ms
  --live / --prepared    Whether use live or prepared backend
  --gui / --nogui        Whether graphical interface should be shown
  --help                 Show this message and exit.
```

## Backends
Backend specifies how possible player moves, terminal states, subsequent game states are calculated. There are two backends implemented:
- **Live** - Everything is calculated on the fly, what is relatively slow.
- **Prepared** - All states, transitions and so on are calculated only once, saved in a file and are fast loaded in subsequent program launches. Require initial delay to build everything, but following games are much faster.

## Obtained results

### Map 5x4
| Algorithm     | win / lost / draw |
| ------------- | ----------------- |
| value\_approx | 85.1 / 12.1 / 2.8 |
| sarsa\_lambda | 49.9 / 46.1 / 4.0 |
| q\_learning   | 49.8 / 46.6 / 3.6 |
| mcts          | 44.7 / 51.1 / 4.2 |

### Map 5x5
| Algorithm     | win / lost / draw |
| ------------- | ----------------- |
| dq\_learning  | 55.6 / 44.3 / 0.1 |
| exp\_sarsa    | 61.8 / 38.0 / 0.2 |
| mcts          | 65.1 / 34.9 / 0.0 |
| q\_learning   | 59.0 / 40.7 / 0.3 |
| sarsa         | 58.2 / 41.5 / 0.3 |
| sarsa\_lambda | 92.3 / 7.6 / 0.1  |
| value\_approx | 89.4 / 10.5 / 0.1 |

### Map 6x6
| Algorithm     | win / lost / draw |
| ------------- | ----------------- |
| value\_approx | 79.3 / 18.0 / 2.7 |
| mcts          | 47.4 / 47.8 / 4.8 |

### Map 8x8
| Algorithm     | win / lost / draw |
| ------------- | ----------------- |
| value\_approx | 85.1 / 12.1 / 2.8 |
| sarsa\_lambda | 49.9 / 46.1 / 4.0 |
| q\_learning   | 49.8 / 46.6 / 3.6 |
| mcts          | 44.7 / 51.1 / 4.2 |

## Requirements
- Python version: `3.10.5`
- Installing requirements: `pip install -r requirements.txt`
