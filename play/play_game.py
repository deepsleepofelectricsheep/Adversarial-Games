from games.quoridor import Quoridor
from games.tictactoe import TicTacToe
from agents.random import RandomAgent
from agents.human import HumanAgent
from agents.mcts import MCTSAgent, QuoridorMCTSAgent
from agents.minmax import QuoridorAlphaBetaAgent, AlphaBetaAgent
import argparse


def initialize_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    # Add game choice arguments
    parser.add_argument('--g', type=str,
                        help='Choice of game.',
                        choices=['Quoridor', 'TicTacToe'],
                        default='Quoridor'
    )

    # Add player choice arguments
    parser.add_argument('--p1', type=str, 
                        help='Choice of player 1.', 
                        choices=['RandomAgent', 'HumanAgent', 'MCTSAgent', 'QuoridorMCTSAgent', 'AlphaBetaAgent', 'QuoridorAlphaBetaAgent'],
                        default='MCTSAgent'
    )
    parser.add_argument('--p2', type=str, 
                        help='Choice of player 2.', 
                        choices=['RandomAgent', 'HumanAgent', 'MCTSAgent', 'QuoridorMCTSAgent', 'AlphaBetaAgent', 'QuoridorAlphaBetaAgent'],
                        default='RandomAgent'
    )

    # Add player settings
    parser.add_argument('--p1_depth', type=int, 
                        help='Depth parameter for rollout. Only applicable if player is an MCTS agent.',
                        default=None
    )
    parser.add_argument('--p2_depth', type=int, 
                        help='Depth parameter for rollout. Only applicable if player is an MCTS agent.',
                        default=None  
    )
    parser.add_argument('--p1_rollouts', type=int,
                        help='Number of rollouts for MCTS. Only applicable if player is an MCTSAgent.',
                        default=100
    )
    parser.add_argument('--p2_rollouts', type=int,
                        help='Number of rollouts for MCTS. Only applicable if player is an MCTSAgent.',
                        default=100
    )


    # Add Quoridor game settings
    parser.add_argument('--s', type=int, 
                        help='Size of Quoridor game board.',
                        choices=[3, 5, 9],
                        default=5
    )
    parser.add_argument('--w', type=int,
                        help='Number of walls',
                        default=5
    )

    return parser


def pprint_actions(game, state):
        # Get all possible actions
        actions = game.actions(state)
        pawn_moves = [move for (move_type, move) in actions if move_type=='pawn']
        h_wall_placements = [move for (move_type, move) in actions if move_type=='h_wall']
        v_wall_placements = [move for (move_type, move) in actions if move_type=='v_wall']
        # Print all possible actions for user
        if len(pawn_moves) > 0:
            print(f'Pawn moves: {str(pawn_moves)[1: -1]}')
        if len(h_wall_placements) > 0:
            print(f'H. wall placements: {str(h_wall_placements)[1: -1]}')
        if len(v_wall_placements) > 0:
            print(f'V. wall placements: {str(v_wall_placements)[1: -1]}')


def play(args):
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
    p1 = p1_cls(game=game, depth=args.p1_depth, rollouts=args.p1_rollouts, player=1)

    p2_cls = globals()[args.p2]
    p2 = p2_cls(game=game, depth=args.p2_depth, rollouts=args.p2_rollouts, player=2)

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