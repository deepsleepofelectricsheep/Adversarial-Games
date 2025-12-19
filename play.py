from games.quoridor import Quoridor
from games.tictactoe import TicTacToe
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.mcts import MCTSAgent, QuoridorMCTSAgent
from agents.minmax import QuoridorAlphaBetaAgent, AlphaBetaAgent
from utils import pprint_actions, initialize_parser
import argparse


def play(args: argparse.Namespace) -> None:
    # Setup game
    g_cls = globals()[args.g]
    game = g_cls(size=args.s, numwalls=args.w)
    state = game.start_state()
    print('The game has begun!')
    print()
    game.visualize(state)
    print()

    # Initialize players
    p1_cls = globals()[args.p1]
    p1 = p1_cls(game=game, depth=args.p1_depth, rollouts=args.p1_rollouts, player=1, policy=args.p1_policy)

    p2_cls = globals()[args.p2]
    p2 = p2_cls(game=game, depth=args.p2_depth, rollouts=args.p2_rollouts, player=2, policy=args.p2_policy)

    # Begin play
    while not game.is_end(state):
        
        # Get action from player 1
        print(f'Player 1: {args.p1}\'s turn.')
        pprint_actions(game, state)
        action = p1.action(state)
        print(f'Player 1: {args.p1} plays: {action}')
        print()

        # Update board
        state = game.successor(state, action)
        game.visualize(state)
        print()

        # Check if game has ended and print message
        if game.is_end(state):
            outcome = f'Player 1: {args.p1} is victorious.' if game.utility(state) == game.win_bonus\
                else f'Player 2: {args.p2} is victorious.' if game.utility(state) == -game.win_bonus\
                else 'It is a draw.'
            print(f'The game has ended. {outcome}')
            break

        # Get action from player 2
        print(f'Player 2: {args.p2}\'s turn.')
        pprint_actions(game, state)
        action = p2.action(state)
        print(f'Player 2: {args.p2} plays: {action}')
        print()

        # Update board
        state = game.successor(state, action)
        game.visualize(state)
        print()

        # Check if game has ended and print message
        if game.is_end(state):
            outcome = f'Player 1: {args.p1} is victorious.' if game.utility(state) == game.win_bonus\
                else f'Player 2: {args.p2} is victorious.' if game.utility(state) == -game.win_bonus\
                else 'It is a draw.'
            print(f'The game has ended. {outcome}')
            break


def main():
    parser = initialize_parser()
    args = parser.parse_args()
    play(args)


if __name__ == '__main__':
    main()