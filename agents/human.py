from agents.base import Agent
from typing import Any, Tuple
import ast


class HumanAgent(Agent):
    def __init__(self, game: Any, player: int = 1, name: str ='Human', *args, **kwargs) -> None:
        self.game = game
        self.player = player
        self.name = name

    def action(self, state: Any) -> Any:
        # Get all possible actions
        actions = self.game.actions(state)
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
        # Get input from user
        while True:
            chosen_movetype = input('Please enter the chosen move type [pawn/h_wall/v_wall]: ')
            if chosen_movetype not in ['pawn', 'h_wall', 'v_wall']:
                print('Invalid move type. Please choose a valid move type from the list above.')
            if chosen_movetype == 'pawn':
                chosen_move = input('Please enter the chosen move: ')
                chosen_move = ast.literal_eval(chosen_move)
                if chosen_move not in pawn_moves:
                    print('Invalid move. Please enter a valid move from the list above.')
                else:
                    return (chosen_movetype, chosen_move)
            elif chosen_movetype == 'h_wall':
                chosen_move = input('Please enter the chosen move: ')
                chosen_move = ast.literal_eval(chosen_move)
                if chosen_move not in h_wall_placements:
                    print('Invalid move. Please enter a valid move from the list above.')
                else:

                    return (chosen_movetype, chosen_move)
            elif chosen_movetype == 'v_wall':
                chosen_move = input('Please enter the chosen move: ')
                chosen_move = ast.literal_eval(chosen_move)
                if chosen_move not in v_wall_placements:
                    print('Invalid move. Please enter a valid move from the list above.')
                else:
                    return (chosen_movetype, chosen_move)
