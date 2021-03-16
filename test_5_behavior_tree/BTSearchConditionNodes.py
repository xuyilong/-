from ConditionNode import ConditionNode
from NodeStatus import *
from ObjectStatus import ObjectStatus
import VrepAPI


# 同理，要将条件也改成节点形式
class IsRobotCloseTo(ConditionNode):
    def __init__(self, name, object_id):
        ConditionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id

        self.flag = 0

    def Execute(self, args):
        if VrepAPI.is_robot_close_2d(self.object_id, 0.1):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class DeliveryObject(ConditionNode):
    def __init__(self, name, object_id, at, object_name):
        ConditionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id
        self.at = at
        self.object_name = object_name

        self.flag = 0

    def Execute(self, args):
        if VrepAPI.are_objects_close2d(self.object_id, self.at, 1) and ObjectStatus.cup_type == 1:
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


class IsObjectAt(ConditionNode):
    def __init__(self, name, object_id, at):
        ConditionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id
        self.at = at

        self.flag = 0

    def Execute(self, args):
        # self.vrep.get_object_grasped_id()  # just for waiting the lock
        if VrepAPI.are_objects_close2d(self.object_id, self.at, 0.12):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)


# self
class TypeOK(ConditionNode):
    def __init__(self, name, object_name):
        ConditionNode.__init__(self, name)
        self.name = name
        self.object_name = object_name

        self.flag = 0

    def Execute(self, args):
        if (self.object_name == 'CoffeeCup' and ObjectStatus.cup_type == 1
                or self.object_name == 'OpenDoor' and ObjectStatus.door_type == 1
                or self.object_name == 'LhHavePot' and ObjectStatus.lh_have_pot_type == 1
                or self.object_name == 'RhHaveCup' and ObjectStatus.rh_have_cup_type == 1
                or self.object_name == 'PathFree' and ObjectStatus.path_free_type == 1
                or self.object_name == 'SearchTable' and ObjectStatus.search_table_type == 1
                or self.object_name == 'SearchRack' and ObjectStatus.search_rack_type == 1
                or self.object_name == 'STForCoffee' and ObjectStatus.st_for_coffee_type == 1
                or self.object_name == 'SRForCoffee' and ObjectStatus.sr_for_coffee_type == 1):
            self.SetStatus(NodeStatus.Success)
            self.SetColor(NodeColor.Green)
        else:
            self.SetStatus(NodeStatus.Failure)
            self.SetColor(NodeColor.Red)

