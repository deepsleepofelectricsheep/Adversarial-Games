# Adapted from Liang's implementation of minmax: https://stanford-cs221.github.io/autumn2025-lectures
from agents.base import Agent
from typing import Any, Tuple
from games.quoridor import State
from heapq import heappush, heappop
    

class AlphaBetaAgent(Agent):
    def __init__(self, game: Any, name: str = 'MinMaxAgent', player: int = 1, depth: int = 4, *args, **kwargs) -> None:
        self.game = game
        self.name = name
        self.player = player
        self.depth = depth if depth else 2

    def action(self, state: Any) -> Any:

        def V_alphabeta(s: Any, d: int, a: float = float('-inf'), b: float = float('inf')) -> Tuple[float, Any]:
            # Check base cases:
            if self.game.is_end(s):
                return self.game.utility(s, self.player), None
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
    # def eval(self, state: Any, player: str | int) -> float:
    #     p1_dist_to_goal = self.game.size - 1 - state.p1[1]
    #     p2_dist_to_goal = state.p2[1]
    #     if player == 1:
    #         return (- 0.5 * p1_dist_to_goal + 0.75 * p2_dist_to_goal)
    #     return (- 0.5 * p2_dist_to_goal + 0.75 * p1_dist_to_goal)

    def eval(self, state: Any, player: str | int) -> float:
        
        p1 = state.p1
        p2 = state.p2
        h_walls = state.h_walls
        v_walls = state.v_walls

        p1_dist_to_goal = self._path_length(p1, p2, h_walls, v_walls, player)
        p2_dist_to_goal = self._path_length(p1, p2, h_walls, v_walls, 2 if player==1 else 1)
        if player == 1:
            return (- 0.5 * p1_dist_to_goal + 0.75 * p2_dist_to_goal)
        return (- 0.5 * p2_dist_to_goal + 0.75 * p1_dist_to_goal)

    def _path_length(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]], player: str | int) -> float:
        
        start = p1 if player == 1 else p2
        goal = self.game.size - 1 if player == 1 else 0

        def _astar(start: Tuple[int, int], goal: int, player: int) -> bool:
            node = start

            if node[1] == goal:
                return 0

            frontier = []
            heappush(frontier, (0, node))
            reached = [node]

            distance = 0

            while len(frontier) > 0:
                g, node = heappop(frontier)

                distance += 1

                # Get children
                state = State(
                    p1=node if player==1 else p2,
                    p2=node if player==2 else p1,
                    p1_numwalls=0,
                    p2_numwalls=0,
                    player=player,
                    h_walls=h_walls,
                    v_walls=v_walls
                )
                actions = self.game.actions(state)
                for action in actions:
                    successor = self.game.successor(state, action)
                    s = successor.p1 if player==1 else successor.p2

                    if s[1] == goal:
                        return distance

                    if s not in reached:
                        reached.append(s)
                        h = _heuristic(s, goal)
                        heappush(frontier, (g + 1 + h, s))
                        
            return float('-inf')     

        def _heuristic(start: Tuple[int, int], goal: int) -> int:
            return abs(goal - start[1])

        return _astar(start, goal, player)