from games.base import AdversarialGame
from typing import Tuple, Any
from dataclasses import dataclass


@dataclass(frozen=True)
class TTCState:
    board: dict
    player: int


class TicTacToe(AdversarialGame):
    def __init__(self, *args, **kwargs) -> None:
        self.possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.columns = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
        self.diags = [[1, 5, 9], [7, 5, 3]]
        self.win_bonus = 1

    def start_state(self) -> TTCState:
        board = {
            1: None, 2: None, 3: None, 
            4: None, 5: None, 6: None, 
            7: None, 8: None, 9: None
        }
        return TTCState(board=board, player=1)
    
    def actions(self, state: TTCState) -> list[int]:
        return [move for move in self.possible_moves if state.board[move] is None]
    
    def successor(self, state: TTCState, action: int) -> TTCState:
        board = {pos: state.board[pos] for pos in state.board}
        board[action] = 'X' if state.player == 1 else 'O'
        return TTCState(board=board, player=2 if state.player==1 else 1)
    
    def player_wins(self, state: TTCState, player: int = 1) -> bool:
        player = 'X' if player == 1 else 'O'

        for row in self.rows:
            if state.board[row[0]] == state.board[row[1]] == state.board[row[2]]:
                if state.board[row[0]] == player:
                    return True
        
        for col in self.columns:
            if state.board[col[0]] == state.board[col[1]] == state.board[col[2]]:
                if state.board[col[0]] == player:
                    return True         

        for diag in self.diags:
            if state.board[diag[0]] == state.board[diag[1]] == state.board[diag[2]]:
                if state.board[diag[0]] == player:
                    return True   

        return False  

    def is_end(self, state: TTCState) -> bool:
        if self.player_wins(state, 1) or self.player_wins(state, 2):
            return True
        if all([state.board[cell] for cell in state.board]):
            return True
        return False
    
    def utility(self, state: TTCState, player: int = 1) -> float:
        if self.player_wins(state, 1):
            return self.win_bonus if player == 1 else -self.win_bonus
        if self.player_wins(state, 2):
            return -self.win_bonus if player == 1 else self.win_bonus
        return 0        
    
    def visualize(self, state: TTCState) -> None:
        for row in self.rows:
            row_print = ''
            for col in row:
                row_print += f' {state.board[col] if state.board[col] else "-"} '
            print(row_print)

    def player(self, state: TTCState) -> None:
        return state.player