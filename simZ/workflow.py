# workflow.py

from typing import Any

import simpy
from .simzdb import SimzDB
from .util.Notify import Notification
from .component import Components


class Workflow:

    def __init__(self,projectname: str, runname: str) -> None:
        self.projectname = projectname
        self.name = runname
        self.env = simpy.Environment()
        self.dbconn = SimzDB()
        self.notif_Channel = Notification()
        self.flow = {}
        self.component_pool: dict[str, Components] = {}

    def add_component(self, component: Components):
        self.component_pool[component.name] = component
    
    def component_validater(self, component: Components):
        pass

    def add_connection(self, component_node):
        pass

    def has_next_components(self):
        pass

    def process_next_component(self, curr_node, payload) :
        pass
