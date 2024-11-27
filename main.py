from dataclasses import dataclass
from typing import Any, Generator, List
import simpy
from simZ.engine import Engine
from simZ.component import Components, ZResource
from simZ.zprocess import TimeOutRunner
from pprint import pprint

inputdata = {
        "cap" : {
            "value": 1,
            "type": int,
            "description": "Resource capacity"
        },
        "queue_limit" : {
            "value": 5,
            "type": int,
            "description": "queue_limit"
        },
        # "dbsave":{
        #     "value": False,
        # }
    }
env = simpy.Environment()
simEngine = Engine()

