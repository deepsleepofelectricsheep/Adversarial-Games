from typing import Any, Tuple
from heapq import heappush, heappop
from games.quoridor import State


def evaluate_state(game: Any, 
                   state: Any, 
                   player: str | int, 
                   weights: list[float] = [0, 0, 0, 0, 0, 0]) -> float:

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

            while len(frontier) > 0:
                g, node = heappop(frontier)

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
                        return g + 1

                    if s not in reached:
                        reached.append(s)
                        h = _heuristic(s, goal)
                        heappush(frontier, (g + 1 + h, s))
                        
            return float('inf')     

        def _heuristic(start: Tuple[int, int], goal: int) -> int:
            return abs(goal - start[1])

        return _astar(start, goal, player)
    
    p1 = state.p1
    p2 = state.p2
    h_walls = state.h_walls
    v_walls = state.v_walls

    my_dist = _path_length(game, p1, p2, h_walls, v_walls, player)
    opp_dist = _path_length(game, p1, p2, h_walls, v_walls, 2 if player==1 else 1)
    my_walls = state.p1_numwalls if player==1 else state.p2_numwalls
    opp_walls = state.p2_numwalls if player==1 else state.p1_numwalls
    my_progress = state.p1[1] if player==1 else game.size - 1 - state.p2[1]
    opp_progress = game.size - 1 - state.p2[1] if player==1 else state.p1[1]

    feature_0 = -my_dist
    feature_1 = opp_dist
    feature_2 = my_walls
    feature_3 = opp_walls
    feature_4 = my_progress
    feature_5 = opp_progress

    return weights[0] * feature_0 \
        + weights[1] * feature_1 \
            + weights[2] * feature_2 \
                + weights[3] * feature_3 \
                    + weights[4] * feature_4 \
                        + weights[5] * feature_5