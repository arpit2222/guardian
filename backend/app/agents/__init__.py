from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """
    Base class for all autonomous agents in SENTINEL.
    """
    def __init__(self):
        self.name = self.__class__.__name__
        
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent's primary function using the provided context.
        Returns a dictionary representing the result.
        """
        pass
