# Adversarial games

## About

This repo contains my explorations of adversarial games. Here I aim to model and solve games, simple and complex, such as Quoridor, applying techniques such as MiniMax and MCTS. I hope you'll enjoy my learning journey. 

Nikhil Raman

## Installation

### pip (Recommended)
```bash
python -m venv venv
source venv/bin/Activate
pip install -e .
```

## Usage

### Example
To start a game of Quoridor between an MCTS agent and an Alpha-beta agent on a board of size 5 with 5 available walls, run the following command from the root of the directory:

```bash
python play/play_game.py --p1 QuoridorMCTSAgent --p1_rollouts 100 --p2 QuoridorAlphaBetaAgent --s 5 --w 5 --p1_depth 50
```

## Acknowledgements
The code in this repo has been adapted from python code for the book "AI: A Modern Approach" (https://github.com/aimacode/aima-python) and python code for Stanford's CS221: AI Principles and Techniques (https://stanford-cs221.github.io/autumn2025-lectures).