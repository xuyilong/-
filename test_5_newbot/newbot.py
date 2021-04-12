import IDList
import FunctionList
import ObjectStatus
import VrepAPI
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import request

app = Flask(__name__)
CORS(app, resources=r'/*')


def id_add(name):
    bname = bytes(name, encoding="utf8")
    gid = FunctionList.get_id(bname)
    return name, gid


@app.route('/hello')
def hello():
    return 'Hello,world!'


@app.route('/s_and_e', methods=['get'])
def s_and_e():
    # print(request.args)
    flag = request.args.get('flag')
    # print('newbot.flag', flag, type(flag))
    FunctionList.fun_s_and_e(flag)
    return 's_and_e'


@app.route('/calling_condition_function', methods=['post'])
def calling_condition_function():
    # print(request.json)
    name = request.json.get('name')
    parm = request.json.get('parm')
    # 在这里使用setattr
    if hasattr(FunctionList, name):
        print('正在执行条件方法')
        if getattr(FunctionList, name)(**parm):
            return 'right'
    else:
        print("------------------------404", '*'*20)
    return 'condition_wrong'


@app.route('/calling_action_function', methods=['post'])
def calling_action_function():
    # print(request.json)
    name = request.json.get('name')
    parm = request.json.get('parm')
    # 在这里使用setattr
    if hasattr(FunctionList, name):
        print('正在执行动作方法')
        getattr(FunctionList, name)(**parm)
    else:
        print("------------------------404", '*'*20)
    return 'action_wrong'


@app.route('/get_list', methods=['get'])
def newbot():
    print('newbot')
    VrepAPI.VrepAPI()

    for item in IDList.IDList.id_list:
        id_name = item.get('name')
        name, gid = id_add(id_name)
        IDList.change_value(name, gid)

    return jsonify(IDList.IDList.id_list, ObjectStatus.ObjectStatus.status_list,
                   FunctionList.FunctionList.action_function_list,
                   FunctionList.FunctionList.condition_function_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# 暂觉得xian应该放这里，并且可以修改move和search的部分
