import argparse
from typing import Any


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
                        default=75
    )
    parser.add_argument('--p2_depth', type=int, 
                        help='Depth parameter for rollout. Only applicable if player is an MCTS agent.',
                        default=75  
    )
    parser.add_argument('--p1_rollouts', type=int,
                        help='Number of rollouts for MCTS. Only applicable if player is an MCTSAgent.',
                        default=100
    )
    parser.add_argument('--p2_rollouts', type=int,
                        help='Number of rollouts for MCTS. Only applicable if player is an MCTSAgent.',
                        default=100
    )
    parser.add_argument('--p1_policy', type=str, 
                        help='Policy for MCTS agent playouts.',
                        choices=['random', 'random_pmove', 'forward_or_random', 'forward_or_random_pmove'],
                        default='random'
    )
    parser.add_argument('--p2_policy', type=str, 
                        help='Policy for MCTS agent playouts.',
                        choices=['random', 'random_pmove', 'forward_or_random', 'forward_or_random_pmove'],
                        default='random'
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

    # Add evaluation settings
    parser.add_argument('--trials', type=int,
                        help='Number of trials.',
                        default=10
    )
    parser.add_argument('--verbose', type=bool,
                        help='Flag to turn on or off printing of per game outcome data.',
                        default=True
    )

    return parser


def pprint_actions(game: Any, state: Any) -> None:
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