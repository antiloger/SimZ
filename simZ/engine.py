# engine.py
from typing import Any, Dict, List, Tuple, Type
from simpy import Environment
import simpy
from .component import Components, ComponentContext
from .workflow import Workflow
from .simzdb import SimzDB
from .util.Notify import Notification

class Engine:

    def __init__(self) -> None:
        self.simulation: object 
        self._componentSlot = {}

    def default_component_register(self):
        """ This cls Register all the default subclasses of Component cls When server is starting """

        for comp_cls in Components.get_all_component():
            type_name = comp_cls.get_type()
            if type_name in self._componentSlot:
                continue
            self._componentSlot[type_name] = comp_cls
    
    def custom_component_register(self, components: List):
        """ This cls Register all the custom subclasses of Component cls When server is starting """

        for comp_cls in components:
            type_name = comp_cls.get_type()
            if type_name in self._componentSlot:
                raise ValueError(f"USER_ERROR: There is already component which has this component name: {type_name}")
            self._componentSlot[type_name] = comp_cls


    def get_all_component(self) -> dict :
        """ to get all compoenent which already registered """
        return self._componentSlot

    def get_component(self, type_name: str) -> Type[Components]:
        if type_name not in self._componentSlot:
            raise ValueError(f"Component type '{type_name}' is not registered!")
        return self._componentSlot[type_name]

    def simDataParser(self, data: Dict[str, Any]):
        # metadata = data["Metadata"]
        componentData = data["Component_Data"]
        connectionData = data["Component_Connection"]
        new_workflow, compCtx = self.MetaDataParser()
        self.ComponentDataParser(new_workflow, compCtx, componentData)
        self.ConnectionDataParser(new_workflow, connectionData)


    def MetaDataParser(self) -> Tuple[Workflow, ComponentContext]:

        # TODO: add data parser
        new_workflow = Workflow("test","test1")
        comp_ctx = ComponentContext(
            env=simpy.Environment(),
            dbconn=SimzDB(),
            notify=Notification(),
            workflow=new_workflow
        )
        return new_workflow, comp_ctx

    def ComponentDataParser(self, workflow: Workflow, ctx: ComponentContext, data: dict[str, List[Any]]):
        for comtype, comdata in data.items():
            typecls = self.get_component(comtype)
            for comp in comdata:
                newtypecls = typecls(comp["name"], ctx, comp["config"])
                workflow.add_component(newtypecls)


    def ConnectionDataParser(self,  workflow: Workflow, data):
        pass

