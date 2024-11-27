from abc import ABC, abstractmethod
from typing import Any, Generator, List
from random import randint
from simpy import Environment


class ZProcess(ABC):
    def __init__(self, env: Environment) -> None:
        self.env = env

    @abstractmethod
    def Run(self, component, items: List[Any], *args: Any) -> Generator :
        ''' 
        yieldable method 
        
        args:
            component: Component[Class]
            items: Items[Class]
            args: Any

        return:
            Generator type
        '''
        pass


class TimeOutRunner(ZProcess):
    def __init__(self, env: Environment, t1: int, t2: int) -> None:
        super().__init__(env)
        self.t1 = t1
        self.t2 = t2

    def Run(self, component, items: List[Any], *args: Any) -> Generator:
        timeYield = randint(self.t1, self.t2)
        yield self.env.timeout(timeYield)

