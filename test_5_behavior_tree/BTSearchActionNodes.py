import requests

from ActionNode import *
from NodeStatus import *
import sys
sys.path.insert(0, 'bt/')


# 创
class SubActionNode(ActionNode):

    def __init__(self, name, **parm):
        ActionNode.__init__(self, name)
        self.name = name
        self.parm = parm['parm']
        for i in self.parm:
            # print('i=', i)
            setattr(self, i, self.parm[i])

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        calling_action_function(self.name, self.parm)
        print('excuting...')


# 一个奇怪的方法
def calling_action_function(name, parm):
    kv = {'name': name, 'parm': parm}
    r = requests.post('http://localhost:5000/calling_action_function', json=kv)
    r.encoding = 'utf-8'
    # print('r:', r.text)


# 应该抽象成action_node
# 因为原数据应该只是功能，但不是节点形式
class MoveCloseTo(ActionNode):

    def __init__(self, name, object_id):
        ActionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        VrepAPI.move_close_to_object(self.object_id)


class MoveCloseToAndSearch(ActionNode):

    def __init__(self, name, object_id, task_name):
        ActionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id
        self.task_name = task_name

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        VrepAPI.move_close_to_and_search(self.object_id, self.task_name)


class PourTo(ActionNode):

    def __init__(self, name):
        ActionNode.__init__(self, name)
        self.name = name

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        VrepAPI.pour_coffee()


class GraspCup(ActionNode):

    def __init__(self, name, object_id):
        ActionNode.__init__(self, name)
        self.name = name
        self.object_id = object_id

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        VrepAPI.grasp_cup(self.object_id)


class OpenDoor(ActionNode):

    def __init__(self, name):
        ActionNode.__init__(self, name)
        self.name = name

    def Execute(self, args):
        self.SetStatus(NodeStatus.Running)
        self.SetColor(NodeColor.Gray)
        VrepAPI.open_door()

