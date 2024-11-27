#component.py

from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional, List, Dict
from pprint import pprint
from simpy import Environment
import uuid
import simpy
from .zprocess import ZProcess
if TYPE_CHECKING:
    from .simzdb import SimzDB
    from .workflow import Workflow

@dataclass
class ComponentConfig:
    attr: Dict[str, Any]
    zprocessors: List[ZProcess]

@dataclass
class ComponentContext:
    env: Environment
    notify: Any
    workflow: 'Workflow'
    dbconn: 'SimzDB'

class Components(ABC):
    def __init__(
        self,
        name: str,
        compCtx: ComponentContext,
        config: ComponentConfig
    ) -> None:
        self.name = name
        self.comType = self.get_type()
        self.id = self._id_generate()
        self.env = compCtx.env
        self.log_buffer = []
        self.g_event: Optional[simpy.Event] = None
        self.notify = compCtx.notify
        self.workflow = compCtx.workflow
        self.simdb = compCtx.dbconn
        self.dbsave = True
        self.ZProcess = None

        self.set_config_data(config)

    def __repr__(self) -> str:
        return f"Component({self.id})"

    @staticmethod
    def _id_generate() -> int:
        return uuid.uuid4().int & ((1 << 32) - 1)
    
    @classmethod
    def get_type(cls) -> str:
        return cls.__name__

    def set_config_data(self, data: ComponentConfig) -> None:
        """Parse configuration data into component attributes."""
        for key, value_dict in data.attr.items():
            if hasattr(self, key):
                setattr(self, key, value_dict["value"])
        
        self.ZProcess = data.zprocessors
    
    @classmethod
    def get_all_component(cls):
        return cls.__subclasses__()

    def inspect(self) -> None:
        """Print component's current state for debugging."""
        pprint(vars(self))

    def next(self, items: List[Any]) -> Generator:
        """Advance workflow to next step."""
        
        if self.workflow.has_next_components():
            yield self.workflow.process_next_component(self.name, items)
        else:
            yield self.env.timeout()

    def notify_send(self, level: int, header: str, body: str) -> None:
        """Send notification with component context."""
        self.notify.send(
            header,
            body,
            {"name": self.name, "id": self.id, "type": self.comType},
            level=level,
        )

    def enter_log(self, action: str, state: Dict[str, Any]) -> None:
        """Log component state change to database."""
        self.log_buffer.append([
            {
                "time" :self.env.now,
                "comp_data": {
                    self.comType,
                    self.name,
                    self.id,
                },
                "action": action,
                "state": state
             }
        ])

    @abstractmethod
    def process(self, items: List[Any]) -> Generator:
        """Process items through this component."""
        pass

class ZResource(Components):

    capacity = 1
    queue_limit = None

    def __init__(
        self,
        name: str,
        ctx: ComponentContext,
        config
    ) -> None:
        super().__init__(name, ctx, config)

        self.res = simpy.Resource(self.env, self.capacity)

    def process(self, items: List[Any]) -> Generator:
        """Process items through the resource with queue management."""
        # if self.queue_limit is not None and len(self.res.queue) >= self.queue_limit:
        #     self.notify_send(3, "Queue Filled", "Queue limit reached")
        #     return

        with self.res.request() as req:
            self.enter_log("IN", {
                "item_ids": [getattr(item, 'id', None) for item in items],
                "queue_length": len(self.res.queue)
            })

            yield req

            if self.ZProcess is not None:
                for proc in self.ZProcess:
                    yield proc.Run(self, items)

        self.enter_log("OUT", {
           "item_ids": [getattr(item, 'id', None) for item in items],
            "queue_length": len(self.res.queue)
        })
        

