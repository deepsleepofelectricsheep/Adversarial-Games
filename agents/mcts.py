# Adapted from Norvig et al's implementation of MCTS: https://github.com/aimacode/
from agents.base import Agent
from typing import Any, Tuple
from collections import defaultdict
import math
import random
        

class Node:
    def __init__(self, state: Any, children: dict = {}, parent: Any = None, U: float = 0, N: float = 0):
        self.state = state
        self.children = children
        self.parent = parent
        self.U = U
        self.N = N


def ucb1(n: Node, c: float = 1.4) -> float:
    if n.N > 0:
        return n.U / n.N + c * math.sqrt(math.log(n.parent.N) / n.N)
    return float('inf')
        

class MCTSAgent:
    def __init__(self, game: Any, name: str = 'MCTSAgent', player: int = 1, rollouts: int = 100, depth: int = 60, *args, **kwargs) -> None:
        self.game = game
        self.name = name
        self.rollouts = rollouts
        self.depth = depth
        self.player = player

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
            player = s.player
            d = 0
            while not self.game.is_end(s) and d < self.depth:
                d += 1
                action = self.policy(s)
                s = self.game.successor(s, action)
            value = self.game.utility(s, player)
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
    

class QuoridorMCTSAgent(MCTSAgent):
    def policy(self, s: Any) -> Tuple[str, Tuple[int, int]]:
        # Prioritize pawn moves in the direction of the goal when possible
        direction = (0, 1) if s.player == 1 else (0, -1)
        actions = self.game.actions(s)
        if ('pawn', direction) in actions:
            return ('pawn', direction)
        else:
            return random.choice(actions)