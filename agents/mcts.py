# Adapted from Norvig et al's implementation of MCTS: https://github.com/aimacode/
from agents.base import Agent
from typing import Any, Tuple
from collections import defaultdict
import math
import random
from agents.utils import evaluate_state
        

class Node:
    def __init__(self, state: Any, parent: Any = None, U: float = 0, N: float = 0):
        self.state = state
        self.parent = parent
        self.U = U
        self.N = N
        self.children = {}


def ucb1(n: Node, c: float = 1.4) -> float:
    if n.N > 0:
        return n.U / n.N + c * math.sqrt(math.log(n.parent.N) / n.N)
    return float('inf')
        

class MCTSAgent:
    def __init__(self, 
                 game: Any, 
                 name: str = 'MCTSAgent', 
                 player: int = 1, 
                 rollouts: int = 100, 
                 depth: int = 60, 
                 policy: str = None, 
                 *args, **kwargs) -> None:
        self.game = game
        self.name = name
        self.rollouts = rollouts
        self.depth = depth if depth else 75
        self.player = player
        self._policy = policy if policy else 'random'

    def action(self, state: Any):

        def select(n: Node) -> Node:
            if n.children:
                return select(max(n.children.keys(), key=ucb1))
            return n

        def expand(n: Node) -> Node:
            if not n.children and not self.game.is_end(n.state):
                n.children = {
                    Node(state=self.game.successor(n.state, action), parent=n): action 
                    for action in self.game.actions(n.state)
                }
            return select(n)

        def simulate(s: Any) -> float:
            player = self.game.player(s)
            d = 0
            while not self.game.is_end(s) and d < self.depth:
                d += 1
                action = self.policy(s)
                s = self.game.successor(s, action)

            if self.game.is_end(s):
                value = self.game.utility(s, player)
            elif d == self.depth:
                value = self.evaluate(s, player)

            value *= (self.depth - d + 1) / self.depth # Winning quickly is better
            return -value

        def backprop(r: float, n: Node):
            n.U += r
            n.N += 1
            if n.parent:
                backprop(-r, n.parent)

        tree = Node(state=state)
        for _ in range(self.rollouts):
            leaf = select(tree)
            child = expand(leaf)
            result = simulate(child.state)
            backprop(result, child)

        action = tree.children[max(tree.children.keys(), key=lambda n: n.N)]
        return action

    def policy(self, state: Any) -> Any:
        return random.choice(self.game.actions(state))
    
    def evaluate(self, state: Any, player: int | str) -> float:
        return self.game.utility(state, player)
    

class QuoridorMCTSAgent(MCTSAgent):
    def policy(self, state: Any) -> Tuple[str, Tuple[int, int]]:

        def _random(state: Any) -> Tuple[str, Tuple[int, int]]:
            return random.choice(self.game.actions(state))
        
        def _random_pmove(state: Any) -> Tuple[str, Tuple[int, int]]:
            return random.choice([(move_type, move) for (move_type, move) in self.game.actions(state) if move_type=='pawn'])
        
        def _forward_or_random(state: Any) -> Tuple[str, Tuple[int, int]]:
            direction = (0, 1) if state.player == 1 else (0, -1)
            moves = self.game.actions(state)
            return ('pawn', direction) if ('pawn', direction) in moves else random.choice(moves)
        
        def _forward_or_random_pmove(state: Any) -> Tuple[str, Tuple[int, int]]:
            direction = (0, 1) if state.player == 1 else (0, -1)
            moves = self.game.actions(state)
            return ('pawn', direction) if ('pawn', direction) in moves\
                else random.choice([(move_type, move) for (move_type, move) in self.game.actions(state) if move_type=='pawn'])
        
        if self._policy == 'random': 
            return _random(state)
        elif self._policy == 'random_pmove':
            return _random_pmove(state)
        elif self._policy == 'forward_or_random':
            return _forward_or_random(state)
        elif self._policy == 'forward_or_random_pmove':
            return _forward_or_random_pmove(state)
        else:
            raise ValueError('Please enter valid policy for MCTS agent.')
        
    def evaluate(self, state: Any, player: int | str) -> float:
        return evaluate_state(self.game, state, player)