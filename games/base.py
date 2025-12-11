from typing import Tuple, Any


class AdversarialGame:
    def start_state(self) -> Any:
        raise NotImplementedError()
    
    def player(self, state: Any) -> int:
        return NotImplementedError()
    
    def action(self, state: Any) -> list[Any]:
        raise NotImplementedError()
    
    def successor(self, state: Any, action: Any) -> Any:
        raise NotImplementedError()
    
    def utility(self, state: Any, player: int) -> float:
        raise NotImplementedError
    
    def is_end(self, state: Any) -> bool:
        raise NotImplementedError()
