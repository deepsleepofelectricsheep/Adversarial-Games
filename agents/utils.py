from typing import Any, Tuple
from heapq import heappush, heappop
from games.quoridor import State


def evaluate_state(game: Any, state: Any, player: str | int) -> float:

    def _path_length(game: Any, 
                     p1: Tuple[int, int], 
                     p2: Tuple[int, int], 
                     h_walls: list[Tuple[int, int]], 
                     v_walls: list[Tuple[int, int]], 
                     player: str | int) -> float:
        
        start = p1 if player == 1 else p2
        goal = game.size - 1 if player == 1 else 0

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
                actions = game.actions(state)
                for action in actions:
                    successor = game.successor(state, action)
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
    
    p1 = state.p1
    p2 = state.p2
    h_walls = state.h_walls
    v_walls = state.v_walls

    p1_dist_to_goal = _path_length(game, p1, p2, h_walls, v_walls, player)
    p2_dist_to_goal = _path_length(game, p1, p2, h_walls, v_walls, 2 if player==1 else 1)
    if player == 1:
        return (- 0.5 * p1_dist_to_goal + 0.75 * p2_dist_to_goal) + 0.5 * state.p1_numwalls / game.numwalls
    return (- 0.5 * p2_dist_to_goal + 0.75 * p1_dist_to_goal) + 0.5 * state.p2_numwalls / game.numwalls