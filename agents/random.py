from agents.base import Agent
from typing import Any
import random


class RandomAgent(Agent):
    def __init__(self, game: Any, name: str ='Random', *args, **kwargs) -> None:
        self.game = game
        self.name = name

    def action(self, state: Any) -> Any:
        actions = self.game.actions(state)
        return random.choice(actions)