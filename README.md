

# Connect Four AI Simulation


https://github.com/user-attachments/assets/6d477863-bbe1-43f9-b703-2243298ef739



This project simulates a Connect Four game between various types of AI players, including Minimax, Q-Learning, Random, and Human players. It uses **Pygame** to create a visual representation of the board and supports different game strategies. The main script can run a series of games and gather statistics on the number of moves and win percentages of the players.

## Features

- AI vs. AI (Minimax with alpha-beta pruning, Q-Learning, Random)
- Board reset and replay
- Statistics on games played (win percentages, average moves)
- Graphical display of the Connect Four board using **Pygame**

## Requirements

- Python 3.8+
- External libraries:
  - `pygame`
  - `numpy`

## Installation

1. Clone the repository:
   ```bash
   git clone <[repo-url](https://github.com/NoorDYahya/Connect-Four-AI.git)>
   cd connect-four-ai
2. Install the required libraries:
   ```bash
   pip install numpy pygame
   

## How to Run

1.Navigate to the directory containing the game files.

2.Run the main.py file:
   ```bash
   python main.py

3.By default, the script will run 100 games between two AI players (Minimax and Random Player). The results will be printed after all games are played.

## Future Work
- Train and include a Q-Learning agent.
- Add more configurable options for game parameters.
- Implement advanced AI strategies for more competitive gameplay like .
