import vrep
import numpy as np
import time
import ObjectStatus
import IDList


# 根据图来确定条件和动作
class FunctionList:
    action_function_list = [
        {'name': 'move_to', 'parm': {'location_id': 0}},
        {'name': 'pour_coffee', 'parm': {'object_id_1': 0, 'object_id_2': 0}},
        {'name': 'grasp', 'parm': {'object_id': 0}},
        {'name': 'open_door', 'parm': {'door_id': 0}},
    ]
    condition_function_list = [
        {'name': 'is_robot_close_to', 'parm': {'location_id': 0}},
        {'name': 'path_free', 'parm': {'location_id': 0}},
        {'name': 'is_open', 'parm': {'door_id': 0}},
        {'name': 'could_open', 'parm': {'door_id': 0}},
        {'name': 'is_hold', 'parm': {'object_id': 0, 'hand_id': 0}},
        {'name': 'is_ready', 'parm': {'object_id': 0, 'object_name': ''}}
    ]


def fun_s_and_e(flag):
    # print('flag', flag, type(flag))
    if flag == '1':
        vrep.simxStartSimulation(IDList.clientID.mainID, vrep.simx_opmode_oneshot)
    elif flag == '0':
        vrep.simxPauseSimulation(IDList.clientID.mainID, vrep.simx_opmode_oneshot)


# 下面部分要传入object_id，是某个场景下获取信息的方式，应该从场景中传入
# 动作节点呢？机器人放入当前场景必然要调试，所以这些应该是在调试过程中加入的
def get_id(name):
    error_id, target_id = vrep.simxGetObjectHandle(IDList.clientID.mainID, name, vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! id:', name, ' is not in the scene', ' and errorID:', error_id)
    else:
        return target_id


# 获取位置
def get_position(object_id, relative_id):
    error_id, position = vrep.simxGetObjectPosition(IDList.clientID.mainID, object_id, relative_id,
                                                    vrep.simx_opmode_oneshot_wait)

    if error_id:
        # raise Exception('Error! cannot retrive pose of' ,object_id)
        return [0, 0, 0]
    else:
        return position


# 获取方向
def get_orientation(object_id, relative_id):
    error_id, orientation = vrep.simxGetObjectOrientation(IDList.clientID.mainID, object_id, relative_id,
                                                          vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot retrive position of', object_id, ' and errorID:', error_id)
    else:
        return orientation


def set_position(object_id, relative_id, position):
    error_id = vrep.simxSetObjectPosition(IDList.clientID.mainID, object_id, relative_id, position,
                                          vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot set position of', object_id, ' and errorID:', error_id)


def set_orientation(object_id, relative_id, orientation):
    error_id = vrep.simxSetObjectOrientation(IDList.clientID.mainID, object_id, relative_id, orientation,
                                             vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot set orientation of', object_id, ' and errorID:', error_id)


# 位置加方向
def get_pose(object_id, relative_id):
    return get_position(object_id, relative_id) + get_orientation(object_id, relative_id)


def set_pose(object_id, relative_id, pose):
    set_position(object_id, relative_id, pose[0:3])
    set_orientation(object_id, relative_id, pose[3:6])


# 因为暂时用不到所以没有改
def close_connection(client_id):
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive.
    # You can guarantee this with (for example):
    vrep.simxGetPingTime(client_id)
    # Now close the connection to V-REP:
    vrep.simxFinish(client_id)
    print('Connection to remote API server closed')


# 好像没用
def are_objects_close(object_1_id, object_2_id, threshold):
    position = get_position(object_1_id, object_2_id)
    return np.linalg.norm(position) < threshold


# 技能 move_close_to_object
def move_to(location_id):
    location_id = int(location_id)
    print('moving close to object', location_id)
    set_pose(IDList.find('newbot_vehicle_target_position'), -1, get_pose(location_id, -1))


# 技能 pour_coffee
def pour_coffee(object_id_1, object_id_2):
    vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 4, vrep.simx_opmode_oneshot_wait)
    time.sleep(35)
    ObjectStatus.change('cup_type', 1)
    time.sleep(5)
    ObjectStatus.change('door_type', 0)


# 技能 grasp_cup
def grasp(object_id):
    object_id = int(object_id)
    if object_id == IDList.find('cup_1'):  # 'cup0_id'
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 3, vrep.simx_opmode_oneshot_wait)
        # 看这里能不能在其他地方改，动作执行完之后
        time.sleep(23)
        ObjectStatus.change('rh_have_cup_type', 1)
    elif object_id == IDList.find('cup_2'):  # 'cup_id'
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 33, vrep.simx_opmode_oneshot_wait)
        time.sleep(20)
        ObjectStatus.change('lh_have_pot_type', 1)
    else:
        print("grasp something wrong!!")


# 技能 这里也可以根据是开的前门还是后门确定
def open_door(door_id):
    if ObjectStatus.find('cup_type') == -1:
        print('open_door something wrong!!!')
    elif ObjectStatus.find('cup_type') == 0:
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 2, vrep.simx_opmode_oneshot_wait)
        # 这里可以改进，不用在这里改door_type，用那个isOpen去调用仿真器吧
        time.sleep(12)
        ObjectStatus.change('door_type', 1)
    else:
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 22, vrep.simx_opmode_oneshot_wait)
        time.sleep(12)
        ObjectStatus.change('door_type', 1)


# 条件 is_robot_close_2d
def is_robot_close_to(location_id):
    # print('success?', object_id)
    # print('type', type(object_id).__name__)
    location_id = int(location_id)
    # print('type', type(object_id))
    position = get_position(location_id, IDList.find('newbot_reference'))
    return np.linalg.norm(position) < 0.2


# 条件 新增
def path_free(location_id):  # cup_1 cup_2 door_1_f door_1_b location_1
    # 根据什么判断呢
    # 暂定 到前后门 1 到杯子门没开 0 到杯子门开了 1
    location_id = int(location_id)
    # print('id__', location_id)
    if location_id == IDList.find('cup_1') or location_id == IDList.find('location_1'):
        if ObjectStatus.find('door_type') == 0:
            return False
        else:
            return True
    if location_id == IDList.find('door_1_f') or location_id == IDList.find('door_1_b'):
        return True
    return True


def is_open(door_id):
    if ObjectStatus.find('door_type') == 1:
        return True
    else:
        return False


def could_open(door_id):
    return True


def is_hold(object_id, hand_id):
    hand_id = int(hand_id)
    if hand_id == IDList.find('left_hand'):
        if ObjectStatus.find('lh_have_pot_type') == 1:
            return True
    if hand_id == IDList.find('right_hand'):
        if ObjectStatus.find('rh_have_cup_type') == 1:
            return True


def is_ready(object_id, object_name):
    # 这里可以调用一个search的方法，然后仿真器执行后返回一个状态
    if ObjectStatus.find('cup_type') == 1:
        return True
    else:
        return False
