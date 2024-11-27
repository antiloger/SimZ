from typing import Any, Generator, List
from simpy import Environment
from ...simZ.component.component import Components


class ZTest(Components):
    def __init__(self, name: str, comp_type: str, env: Environment, action: List[str], notify: Any, workflow: Any, dbconn: Any) -> None:
        super().__init__(name, comp_type, env, action, notify, workflow, dbconn)

    def process(self, items: List[Any]) -> Generator:
        return super().process(items)
