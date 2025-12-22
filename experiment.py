from games.quoridor import Quoridor
from games.tictactoe import TicTacToe
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.mcts import MCTSAgent, QuoridorMCTSAgent
from agents.minmax import QuoridorAlphaBetaAgent, AlphaBetaAgent
from utils import initialize_parser
import argparse
import time
import os


def evaluate(args: argparse.Namespace) -> None:

    verbose = args.verbose

    # Setup game
    trials = args.trials
    g_cls = globals()[args.g]
    game = g_cls(size=args.s, numwalls=args.w)

    # Initialize players
    p1_cls = globals()[args.p1]
    p1 = p1_cls(game=game, depth=args.p1_depth, rollouts=args.p1_rollouts, player=1, policy=args.p1_policy)

    p2_cls = globals()[args.p2]
    p2 = p2_cls(game=game, depth=args.p2_depth, rollouts=args.p2_rollouts, player=2, policy=args.p2_policy)    

    if verbose:
        print()
        print('Arguments:')
        for arg in vars(args): 
            print(f'\t{arg}: {vars(args)[arg]}')
        print()

    # Begin trials
    p1_wins = 0
    p1_move_times = []
    p2_move_times = []
    game_length = []

    for _ in range(trials):

        moves = 0

        # Begin play
        state = game.start_state()
        while not game.is_end(state):

            moves += 1

            start = time.time()
            action = p1.action(state)
            end = time.time()
            p1_move_times.append(end-start)

            state = game.successor(state, action)

            if game.is_end(state):
                p1_wins += 1 if game.utility(state) == game.win_bonus else 0
                break

            start = time.time()
            action = p2.action(state)
            end = time.time()
            p2_move_times.append(end-start)

            state = game.successor(state, action)

            if game.is_end(state):
                p1_wins += 1 if game.utility(state) == game.win_bonus else 0
                break

            if moves > 200:
                p1_wins += 0.5
                break

        if verbose:
            if game.utility(state) == game.win_bonus:
                print(f'Game #{_ + 1} has ended. Player 1: {args.p1} won. The game lasted {moves} moves.')
            elif game.utility(state) == -game.win_bonus:
                print(f'Game #{_ + 1} has ended. Player 2: {args.p2} won. The game lasted {moves} moves.')
            else:
                print(f'Game #{_ + 1} has ended. The game length exceeded 200 moves. The game was called a draw.')
            print()

        game_length.append(moves)

    # Print statistics
    print(f'Evaluation concluded! Outcomes:')
    print(f'\tGames played: {trials}.')
    print(f'\tPlayer 1: {args.p1} won {p1_wins} games.')
    print(f'\tPlayer 2: {args.p2} won {trials-p1_wins} games.')
    print(f'\tOn average, player 1 took {round(sum(p1_move_times) / len(p1_move_times), 2)} seconds per move.')
    print(f'\tOn average, player 2 took {round(sum(p2_move_times) / len(p2_move_times), 2)} seconds per move.')
    print(f'\tThe average game was {round(sum(game_length) / len(game_length))} moves long.')


def main():
    parser = initialize_parser()
    args = parser.parse_args()
    evaluate(args)


if __name__ == '__main__':
    main()
