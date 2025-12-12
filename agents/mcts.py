# Adapted from Norvig et al's implementation of MCTS: https://github.com/aimacode/
from agents.base import Agent
from typing import Any, Tuple
from collections import defaultdict
import math
import random


# Basic datastructure for MCTS
class Node:
    def __init__(self, state: Any, parent: Any = None, U: float = 0, N: int = 0):
        self.state = state
        self.parent = parent 
        self.children = {} # Node: action
        self.action = None
        self.U = U
        self.N = N


# UCB1 (Upper confidence bounds applied to trees)
def ucb1(node: Node, C: float = math.sqrt(1)) -> float:
    if node.N > 0:
        return node.U / node.N + C * math.sqrt(math.log(node.parent.N) / node.N)
    return float('inf')


# MCTS Agent
class MCTSAgent(Agent):
    def __init__(self, game: Any, name: str = 'MCTSAgent', player: int = 1, rollouts: int = 100, depth: int = None, *args, **kwargs) -> None:
        self.game = game
        self.name = name
        self.player = player
        self.rollouts = rollouts
        self.depth = depth if depth else float('inf')

    def action(self, state: Any) -> Any:

        def _select(n: Node) -> Node:
            # Take a tree and return the leaf with the max UCB1 score
            if n.children:
                return _select(max(n.children.keys(), key=ucb1))
            return n
        
        def _expand(n: Node) -> Node:
            # Grow the search tree by creating a new child of the selected node
            if not n.children and not self.game.is_end(n.state):
                n.children = {
                    Node(self.game.successor(n.state, action), parent=n): action\
                        for action in self.game.actions(n.state)
                }
            return _select(n)
        
        def _simulate(s: Any, depth: int) -> Tuple[float, int]:
            # Perform a rollout and return utility
            player = self.game.player(s)
            d = 0
            while not self.game.is_end(s) and d < depth:
                d += 1
                a = random.choice(self.game.actions(s))
                s = self.game.successor(s, a)
            return -self.game.utility(s, player)
        
        def _backprop(r: float, n: Node) -> None:
            # Update the selected branch of the tree based on outcome of rollout
            if r > 0:
                n.U += r
            n.N += 1
            if n.parent:
                _backprop(-r, n.parent)

        tree = Node(state=state)
        for i in range(self.rollouts):
            leaf = _select(tree)
            child = _expand(leaf)
            result = _simulate(child.state, self.depth)
            _backprop(result, child)

        action = tree.children[max(tree.children.keys(), key=lambda r: r.N)]
        return action