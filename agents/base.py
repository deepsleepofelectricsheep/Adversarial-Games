from typing import Any


class Agent:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def action(self, state: Any) -> Any:
        return NotImplementedError()