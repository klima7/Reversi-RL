# Reversi

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
