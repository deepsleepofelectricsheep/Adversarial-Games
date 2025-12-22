# Adapted from Liang's implementation of minmax: https://stanford-cs221.github.io/autumn2025-lectures
from agents.base import Agent
from typing import Any, Tuple
from agents.utils import evaluate_state
    

class AlphaBetaAgent(Agent):
    def __init__(self, 
                 game: Any, 
                 name: str = 'MinMaxAgent', 
                 player: int = 1, 
                 depth: int = 4, 
                 *args, **kwargs) -> None:
        self.game = game
        self.name = name
        self.player = player
        self.depth = depth if depth else 2

    def action(self, state: Any) -> Any:

        def V_alphabeta(s: Any, d: int, a: float = float('-inf'), b: float = float('inf')) -> Tuple[float, Any]:
            # Check base cases:
            if self.game.is_end(s):
                return self.game.utility(s, self.player) * 100, None
            if d == 0:
                return self.eval(s, self.player), None
            
            # Recursive cases:
            actions_and_successors = [(action, self.game.successor(s, action)) for action in self.game.actions(s)]

            if s.player == self.player:
                best_value, best_action = float('-inf'), None
                for action, successor in actions_and_successors:
                    value, _ = V_alphabeta(successor, d-1, a, b)
                    if value > best_value:
                        best_value, best_action = value, action
                    a = max(a, best_value)
                    if a >= b:
                        break
                return best_value, best_action
            
            if s.player != self.player:
                worst_value, worst_action = float('inf'), None
                for action, successor in actions_and_successors:
                    value, _ = V_alphabeta(successor, d-1, a, b)
                    if value < worst_value:
                        worst_value, worst_action = value, action
                    b = min(b, worst_value)
                    if a >= b:
                        break
                return worst_value, worst_action            
        
        return V_alphabeta(state, self.depth)[1]
    
    def eval(self, state: Any, player: str | int) -> float:
        return 0


class QuoridorAlphaBetaAgent(AlphaBetaAgent):
    def eval(self, state: Any, player: str | int) -> float:
        return evaluate_state(self.game, state, player, [0.5, 0.5, 0.1, 0.1, 0.05, 0.05])