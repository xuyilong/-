from BTSearchActionNodes import *
from BTSearchConditionNodes import *
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import request
import requests

from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from NewDraw import new_draw_tree
from global_var import GlobalVar
from FailNode import FailNode

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/hello', methods=['get'])
def hello():
    return 'Hello,world!'


@app.route('/sendGoalNode', methods=['post'])
def receive_goal_node():
    Node.goal_node = request.json
    return 'sendGoalNode'


@app.route('/sendSubtreeList', methods=['post'])
def receive_subtree():
    # print(request.json)
    # 获得后应存储在一个地方
    GlobalVar.subtree_list = request.json
    return 'sendSubtreeList'


@app.route('/start_and_end', methods=['get'])
def receive_start_and_end_signal():
    Node.flag = request.args.get('sig')
    # print('flag.type', Node.flag, type(Node.flag))
    s_and_e(Node.flag)
    if Node.done == 0 and Node.flag == '1':
        init_tree()
        Node.done = 1
    elif Node.flag == '1':
        execute(Node.root)
    print('start_and_end 结束')
    return 'start_and_end'


class Node:
    root = None
    goal_node = {}
    done = 0
    flag = ''


# 控制仿真的开始与暂停
def s_and_e(flag):
    r = requests.get('http://localhost:5000/s_and_e?flag='+flag)
    r.encoding = 'utf-8'
    # print('r:', r.text)
    return r.text


def execute(root):
    while Node.flag == '1':
        # 传输控制信号
        print('-------------执行前------------------')
        while Node.flag == '1':
            root.Execute(None)
            time.sleep(1)
            if root.GetStatus() == 1:
                break

        print('-------------执行后-----------------')

        if FailNode.failChildNode is None:
            return 0
        childNode = FailNode.failChildNode
        fatherNode = FailNode.failFatherNode
        childAddress = FailNode.address

        # 要找到它自己的根 暂不考虑冲突
        # subTree = expandTree(childNode)
        subTree = new_expand_tree(childNode)
        fatherNode.RemoveChild(childNode)
        fatherNode.AddChild(subTree, childAddress)
    return 0


# execute
def init_tree():
    # print('now test execution')
    # print('读取到的GoalNode:', Node.goal_node)
    Node.root = FallbackNode('root')
    # 在这里添加目标节点
    if Node.goal_node != {}:
        goal_node = SubConditionNode(**Node.goal_node)
        Node.root.AddChild(goal_node)
        Node.goal_node = {}

    draw_thread = threading.Thread(target=new_draw_tree, args=(Node.root,))
    draw_thread.start()

    execute(Node.root)


# 暂写，不一定正确
def new_expand_tree(node):
    print('newExpandTree')
    subtree = FallbackNode('Fallback')
    subtree.AddChild(node)
    sequence = SequenceNode('Sequence')
    # 要考虑没有动作节点的情况
    for item in GlobalVar.subtree_list:
        # print('item', item)
        pnode = item.get('post_condition')

        if pnode.get('name') == node.name and pnode.get('parm') == node.parm:
            pre_condition_list = item.get('pre_condition_list')
            for i in pre_condition_list:
                sequence.AddChild(SubConditionNode(**i))
            if item.get('skill').get('name') != '':
                skill = SubActionNode(**item.get('skill'))
                sequence.AddChild(skill)
    subtree.AddChild(sequence)
    return subtree


def test():
    action = SubActionNode(**{'name': 'move_and_search', 'parm': {'object_id': 0, 'task_name': 'MASTable'}})
    # print_object(action)
    print('How about this one', action.name)


def print_object(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


if __name__ == "__main__":
    # test()
    app.run(host='0.0.0.0', port=5001, debug=True)


