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
from FailNode import FailNode
import toDB
import knowledge
import copy

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/hello', methods=['get'])
def hello():
    return 'Hello,world!'


# 发送给前端的子树
@app.route('/get_subtree_list', methods=['get'])
def get_subtree_list():
    print('get_subtree_list')

    return jsonify(Node.subtree_list)


# 从前端接收目标节点
@app.route('/sendGoalNode', methods=['post'])
def receive_goal_node():
    Node.goal_node = request.json
    print('goal_node', Node.goal_node)
    return 'sendGoalNode'


# 从前端接收的子树
@app.route('/sendSubtreeList', methods=['post'])
def receive_subtree():
    # print(request.json)
    # 获得后应存储在一个地方  应该涉及到持久化
    tem_subtree_list = request.json
    toDB.add(tem_subtree_list)
    # print('subtree_list', Node.subtree_list)
    toDB.look()
    Node.subtree_list = toDB.get_all()
    # Node.subtree_list = request.json
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
    subtree_list = toDB.get_all()
    done = 0
    flag = ''


# 控制仿真的开始与暂停
def s_and_e(flag):
    r = requests.get('http://localhost:5000/s_and_e?flag='+flag)
    r.encoding = 'utf-8'
    # print('r:', r.text)
    return r.text


# 循环执行树
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

        if FailNode.failChildNode is None or root.GetStatus() != 1:
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


# execute，首次执行时，初始化环境
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


# 当树的执行失败时扩展树
def new_expand_tree(node):
    print('newExpandTree')
    # 应该只用在这里修改
    # 如果是不传参数的版本，应该有更复杂的处理，传进来的带参目标
    # 根据目标名字找子树，找到后添加相应节点，节点的参数由上方传输
    # 先根据例子做简单处理
    subtree = FallbackNode('Fallback')
    subtree.AddChild(node)
    sequence = SequenceNode('Sequence')
    # 要考虑没有动作节点的情况
    # print('list', Node.subtree_list)
    # 这是在list中寻找
    have_sub = 0
    for item in Node.subtree_list:
        # print('item', item)
        pnode = item[1].get('post_condition')
        print('pnode', pnode)

        if pnode.get('name') == node.name:
            have_sub = 1
            pre_condition_list = item[1].get('pre_condition_list')
            for i in pre_condition_list:
                # 这里替换节点的相应参数
                new_i = transmit_parm(node, i)
                sequence.AddChild(SubConditionNode(**new_i))
            sk = item[1].get('skill')
            if sk.get('name') != '':
                have_sub = 1
                new_sk = transmit_parm(node, sk)
                skill = SubActionNode(**new_sk)
                sequence.AddChild(skill)
    # 如果子树列表中没有，那么就寻找知识
    if have_sub == 0:
        sublist = knowledge.find_from_know(node)
        for item in sublist:
            sequence.AddChild(SubConditionNode(**item))
    subtree.AddChild(sequence)
    return subtree


# 这里是在list中能找到的情况，如果找不到就不会进入这里了
# 根据子节点的参数值寻找父节点的参数值
# 由于python的机制，在调用函数中修改传入字典的值，原字典就会被修改，所以不用再回传
# 由于这个机制，我们应该再复制一个，而不能让列表中的数据变化
def transmit_parm(fnode, cdic):
    new_dic = copy.deepcopy(cdic)
    cparm = new_dic.get('parm')
    for key, value in cparm.items():
        tem_v = getattr(fnode, value)
        print('tem_v', tem_v)
        cparm[key] = tem_v
    return new_dic


# 测试节点是否创建成功
def test():
    action = SubActionNode(**{'name': 'move_and_search', 'parm': {'object_id': 0, 'task_name': 'MASTable'}})
    # print_object(action)
    print('How about this one', action.name)


def print_object(obj):
    print('\n'.join(['%s:%s' % item for item in obj.__dict__.items()]))


if __name__ == "__main__":
    # test()
    print(Node.subtree_list)
    app.run(host='0.0.0.0', port=5001, debug=True)



