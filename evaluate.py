from games.quoridor import Quoridor
from games.tictactoe import TicTacToe
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.mcts import MCTSAgent, QuoridorMCTSAgent
from agents.minmax import QuoridorAlphaBetaAgent, AlphaBetaAgent
from utils import initialize_parser
import argparse
import time


def evaluate(args: argparse.Namespace) -> None:
    # Setup game
    trials = args.trials
    g_cls = globals()[args.g]
    game = g_cls(size=args.s, numwalls=args.w)

    # Initialize players
    p1_cls = globals()[args.p1]
    p1 = p1_cls(game=game, depth=args.p1_depth, rollouts=args.p1_rollouts, player=1, policy=args.p1_policy)

    p2_cls = globals()[args.p2]
    p2 = p2_cls(game=game, depth=args.p2_depth, rollouts=args.p2_rollouts, player=2, policy=args.p2_policy)    

    # Begin trials
    p1_wins = 0
    p1_move_times = []
    p2_move_times = []

    for _ in range(trials):

        # Begin play
        state = game.start_state()
        while not game.is_end(state):

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

    # Print statistics
    print(f'Evaluation concluded.')
    print(f'\tGames played: {trials}.')
    print(f'\tPlayer 1: {args.p1} won {p1_wins} games.')
    print(f'\tPlayer 2: {args.p2} won {trials-p1_wins} games.')
    print(f'\tOn average, player 1 took {round(sum(p1_move_times) / len(p1_move_times), 2)} seconds per move.')
    print(f'\tOn average, player 2 took {round(sum(p2_move_times) / len(p2_move_times), 2)} seconds per move.')


def main():
    parser = initialize_parser()
    args = parser.parse_args()
    evaluate(args)


if __name__ == '__main__':
    main()
