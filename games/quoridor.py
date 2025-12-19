from dataclasses import dataclass
from typing import Tuple, Any
from games.base import AdversarialGame
import random
from heapq import heappush, heappop


@dataclass(frozen=True)
class State:
    # Basic state definition for Quoridor game
    p1: Tuple[int, int] # (x, y)
    p2: Tuple[int, int]
    p1_numwalls: int
    p2_numwalls: int
    player: int 
    h_walls: frozenset
    v_walls: frozenset

    def __lt__(self, other) -> bool: # To prevent errors later
        return True


class Quoridor(AdversarialGame):
    def __init__(self, size=5, numwalls=3) -> None:
        self.size = size
        self.numwalls = numwalls
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.win_bonus = 1

        # Precompute valid wall positions
        self.wall_placement_candidates = [
            (i, j) for i in range(self.size - 1) for j in range(self.size - 1)
        ]

    def start_state(self) -> State:
        mid = self.size // 2
        return State(
            p1=(mid, 0),
            p2=(mid, self.size-1),
            p1_numwalls=self.numwalls,
            p2_numwalls=self.numwalls,
            player=1,
            h_walls=frozenset(),
            v_walls=frozenset()
        )
    
    def is_end(self, state: State) -> bool:
        return True if state.p1[1]==self.size-1 or state.p2[1]==0 else False
    
    def utility(self, state: State, player: int = 1) -> float:
        if player == 1:
            return self.win_bonus if state.p1[1]==self.size-1 else -self.win_bonus if state.p2[1]==0 else 0
        return -self.win_bonus if state.p1[1]==self.size-1 else self.win_bonus if state.p2[1]==0 else 0

    def _hop_straight(self, direction: Tuple[int, int]) -> Tuple[int, int]:
        if direction == (0, 1):
            return (0, 2)
        if direction == (0, -1):
            return (0, -2)
        if direction == (1, 0):
            return (2, 0)
        if direction == (-1, 0):
            return (-2, 0)
        
    def _hop_diagonally(self, direction: Tuple[int, int]) -> list[Tuple[int, int]]:
        if direction == (0, 1):
            return [(1, 1), (-1, 1)]
        if direction == (0, -1):
            return [(1, -1), (-1, -1)]
        if direction == (1, 0):
            return [(1, 1), (1, -1)]
        if direction == (-1, 0):
            return [(-1, 1), (-1, -1)]      

    def _is_blocked(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]]) -> bool:

        if p1[0] == p2[0]:
            for wall in h_walls:
                if wall[0] == p1[0] or wall[0] == p1[0] - 1:
                    if wall[1] == min(p1[1], p2[1]):
                        return True
                    
        if p1[1] == p2[1]:
            for wall in v_walls:
                if wall[1] == p1[1] or wall[1] == p1[1] - 1:
                    if wall[0] == min(p1[0], p2[0]):
                        return True        

        return False
    
    def _path_exists_bfs(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]]) -> bool:
        # Implement BFS to ensure at least 1 path exists to the goal
        def _bfs(start: Tuple[int, int], goal: int, player: int) -> bool:
            node = start
            if node[1] == goal:
                return True
            frontier = [node]
            reached = [node]
            while len(frontier) > 0:
                node = frontier.pop()
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
                actions = self.actions(state)
                for action in actions:
                    successor = self.successor(state, action)
                    s = successor.p1 if player==1 else successor.p2
                    if s[1] == goal:
                        return True
                    if s not in reached:
                        reached.append(s)
                        frontier.append(s)
            return False
        
        # If there's a path for both players, then return true, otherwise false
        if _bfs(p1, self.size-1, 1) and _bfs(p2, 0, 2):
            return True 
        
        return False
    
    def _path_exists_astar(self, p1: Tuple[int, int], p2: Tuple[int, int], h_walls: list[Tuple[int, int]], v_walls: list[Tuple[int, int]]) -> bool:
        # Implement BFS to ensure at least 1 path exists to the goal
        def _astar(start: Tuple[int, int], goal: int, player: int) -> bool:
            node = start
            if node[1] == goal:
                return True
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
                actions = self.actions(state)
                for action in actions:
                    successor = self.successor(state, action)
                    s = successor.p1 if player==1 else successor.p2
                    if s[1] == goal:
                        return True
                    if s not in reached:
                        reached.append(s)
                        h = _heuristic(s, goal)
                        heappush(frontier, (g + 1 + h, s))

            return False
        
        def _heuristic(start: Tuple[int, int], goal: int) -> int:
            return abs(goal - start[1])
        
        # If there's a path for both players, then return true, otherwise false
        if _astar(p1, self.size-1, 1) and _astar(p2, 0, 2):
            return True 
        
        return False
        
    def _in_bounds(self, p: Tuple[int, int]) -> bool:
        if p[0] < self.size and p[0] >= 0:
            if p[1] < self.size and p[1] >= 0:
                return True
            
        return False
    
    def _get_pawn_moves(self, state: State) -> list[Tuple[int, int]]:

        legal_pawn_moves = []

        # Happy path: orthogonal square is within bounds and neither blocked nor occupied by opponent
        for direction in self.directions:
            successor = self.successor(state, ('pawn', direction))
            if successor.p1 != successor.p2:
                if self._in_bounds(successor.p1) and self._in_bounds(successor.p2):
                    if self.player(state) == 1:
                        if not self._is_blocked(state.p1, successor.p1, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)
                    elif self.player(state) == 2:
                        if not self._is_blocked(state.p2, successor.p2, state.h_walls, state.v_walls):
                            legal_pawn_moves.append(direction)      

        # Unhappy path: orthogonal square is occupied by opponent
        for direction in self.directions:
            successor = self.successor(state, ('pawn', direction))
            if successor.p1 == successor.p2:
                pc = state.p1 if self.player(state) == 1 else state.p2
                if not self._is_blocked(pc, successor.p2, state.h_walls, state.v_walls):
                    # First, try hopping straight
                    failed = True
                    hop = self._hop_straight(direction)
                    successor = self.successor(state, ('pawn', hop))
                    if self._in_bounds(successor.p1) and self._in_bounds(successor.p2):
                        if self.player(state) == 1:
                            if not self._is_blocked(state.p2, successor.p1, state.h_walls, state.v_walls):
                                legal_pawn_moves.append(hop)
                                failed = False
                        elif self.player(state) == 2:
                            if not self._is_blocked(state.p1, successor.p2, state.h_walls, state.v_walls):
                                legal_pawn_moves.append(hop)
                                failed = False

                    # Next, try hopping diagonally
                    if failed:
                        for hop in self._hop_diagonally(direction):
                            successor = self.successor(state, ('pawn', hop))
                            if self._in_bounds(successor.p1) and self._in_bounds(successor.p2):
                                if self.player(state) == 1:
                                    if not self._is_blocked(state.p2, successor.p1, state.h_walls, state.v_walls):
                                        legal_pawn_moves.append(hop)
                                elif self.player(state) == 2:
                                    if not self._is_blocked(state.p1, successor.p2, state.h_walls, state.v_walls):
                                        legal_pawn_moves.append(hop)

        return legal_pawn_moves
    
    def _get_h_wall_placements(self, state: State) -> list[Tuple[int, int]]:
        
        legal_placements = []

        if self.player(state) == 1:
            if state.p1_numwalls <= 0:
                return legal_placements
            
        if self.player(state) == 2:
            if state.p2_numwalls <= 0:
                return legal_placements

        for candidate in self.wall_placement_candidates:
            if candidate not in state.h_walls:
                if candidate not in [(wall[0]+1, wall[1]) for wall in state.h_walls]:
                    if candidate not in [(wall[0]-1, wall[1]) for wall in state.h_walls]:
                        if candidate not in state.v_walls:
                            successor = self.successor(state, ('h_wall', candidate))
                            if self._path_exists_astar(successor.p1, successor.p2, successor.h_walls, successor.v_walls):
                                legal_placements.append(candidate)

        return legal_placements
    
    def _get_v_wall_placements(self, state: State) -> list[Tuple[int, int]]:
        
        legal_placements = []

        if self.player(state) == 1:
            if state.p1_numwalls <= 0:
                return legal_placements
            
        if self.player(state) == 2:
            if state.p2_numwalls <= 0:
                return legal_placements

        for candidate in self.wall_placement_candidates:
            if candidate not in state.v_walls:
                if candidate not in [(wall[0], wall[1]+1) for wall in state.v_walls]:
                    if candidate not in [(wall[0], wall[1]-1) for wall in state.v_walls]:
                        if candidate not in state.h_walls:
                            successor = self.successor(state, ('v_wall', candidate))
                            if self._path_exists_astar(successor.p1, successor.p2, successor.h_walls, successor.v_walls):
                                legal_placements.append(candidate)

        return legal_placements  

    def actions(self, state: State) -> list[Tuple[str, Any]]:
        actions = []

        # Pawn moves
        pawn_moves = self._get_pawn_moves(state) 
        for pawn_move in pawn_moves:
            actions.append(('pawn', pawn_move))

        # Horizontal wall placements
        h_wall_placements = self._get_h_wall_placements(state)
        for h_wall_placement in h_wall_placements:
            actions.append(('h_wall', h_wall_placement))

        # Vertical wall placements
        v_wall_placements = self._get_v_wall_placements(state)
        for v_wall_placement in v_wall_placements:
            actions.append(('v_wall', v_wall_placement))

        return actions
    
    def successor(self, state: State, action: Tuple[str, Any]) -> State:
        move_type, move = action

        # Move was a pawn move
        if move_type == 'pawn':
            return State(
                p1=(state.p1[0]+move[0], state.p1[1]+move[1]) if self.player(state)==1 else state.p1,
                p2=(state.p2[0]+move[0], state.p2[1]+move[1]) if self.player(state)==2 else state.p2,
                player=1 if self.player(state)==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls,
                p2_numwalls=state.p2_numwalls,
                h_walls=state.h_walls,
                v_walls=state.v_walls
            )
        
        # Move was a h_wall placement
        if move_type == 'h_wall':
            h_walls = [h_wall for h_wall in state.h_walls]
            h_walls.append(move)
            return State(
                p1=state.p1,
                p2=state.p2,
                player=1 if self.player(state)==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls-1 if self.player(state)==1 else state.p1_numwalls,
                p2_numwalls=state.p2_numwalls-1 if self.player(state)==2 else state.p2_numwalls,
                h_walls=frozenset(h_walls),
                v_walls=state.v_walls
            )
        
        # Move was a v_wall placement
        if move_type == 'v_wall':
            v_walls = [v_wall for v_wall in state.v_walls]
            v_walls.append(move)
            return State(
                p1=state.p1,
                p2=state.p2,
                player=1 if self.player(state)==2 else 2, # Switch turns
                p1_numwalls=state.p1_numwalls-1 if self.player(state)==1 else state.p1_numwalls,
                p2_numwalls=state.p2_numwalls-1 if self.player(state)==2 else state.p2_numwalls,
                h_walls=state.h_walls,
                v_walls=frozenset(v_walls)
            )
        
        # Unknown move type
        else: 
            raise ValueError('Invalid move type.')
        
    def player(self, state: State) -> int:
        return state.player
        
    def visualize(self, state: State) -> None:

        for y in reversed(range(self.size)):
            row = f'{y} '
            for x in range(self.size):
                # Draw players
                if state.p1 == (x, y):
                    row += 'X'
                elif state.p2 == (x, y):
                    row += 'O'
                else:
                    row += '.'
                
                # Draw vertical walls to the right of the marker
                if (x, y) in state.v_walls or (x, y-1) in state.v_walls:
                    row += '|'
                else:
                    row += ' '

            print(row)

            # Draw horizontal walls below the marker
            row = '  '
            for x in range(self.size):
                if (x, y-1) in state.h_walls or (x-1, y-1) in state.h_walls:
                    row += '--'
                else:
                    row += '  '
            print(row)   

        footer = '  ' + ' '.join([str(x) for x in range(self.size)])
        print(footer)

       