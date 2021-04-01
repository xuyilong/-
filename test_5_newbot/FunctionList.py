import vrep
import numpy as np
import time
import ObjectStatus
import IDList


class FunctionList:
    action_function_list = [
        {'name': 'move_to', 'parm': {'object_id': 0}},
        {'name': 'move_and_search', 'parm': {'object_id': 0, 'task_name': 'MASTable'}},
        {'name': 'pour', 'parm': {}},
        {'name': 'grasp', 'parm': {'object_id': 0}},
        {'name': 'open_door', 'parm': {}},
    ]
    condition_function_list = [
        {'name': 'is_robot_close_to', 'parm': {'object_id': 0}},
        {'name': 'delivery_object', 'parm': {'object_id': 0, 'location_id': 0, 'object_name': 'CoffeeCup'}},
        {'name': 'is_object_at', 'parm': {'object_id': 0, 'location_id': 0}},
        {'name': 'type_ok', 'parm': {'object_name': 'CoffeeCup'}},
    ]


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


def get_closest_inverse_pose(object_id, ref_id, type='cube'):
    if type is 'cube':
        z_shift = -0.03
    elif type is 'goal':
        z_shift = 0

    distance = 10000000000
    closest_inverse_pose = None
    dummy_id = get_id(b'Disc')
    shift = 0

    # shift in x
    empty_position = [0, 0, -0.03, 0, 0, 0]
    empty_position[0] += shift
    set_pose(dummy_id, object_id, empty_position)
    set_orientation(dummy_id, object_id, [0, 0, 3.14 / 2])

    dummy_rel_position = get_position(dummy_id, ref_id)
    dummy_distance = np.linalg.norm(dummy_rel_position)
    if dummy_distance < distance:
        closest_inverse_pose = get_pose(dummy_id, -1)
        distance = dummy_distance

    empty_position = [0, 0, -0.03, 0, 0, 0]
    empty_position[0] -= shift

    set_pose(dummy_id, object_id, empty_position)
    set_orientation(dummy_id, object_id, [0, 0, -3.14 / 2])
    dummy_rel_position = get_position(dummy_id, ref_id)
    dummy_distance = np.linalg.norm(dummy_rel_position)
    if dummy_distance < distance:
        closest_inverse_pose = get_pose(dummy_id, -1)
        distance = dummy_distance

    # shift in y
    empty_position = [0, 0, -0.03, 0, 0, 0]
    empty_position[1] += shift
    set_pose(dummy_id, object_id, empty_position)
    set_orientation(dummy_id, object_id, [0, 0, 3.14])

    dummy_rel_position = get_position(dummy_id, ref_id)
    dummy_distance = np.linalg.norm(dummy_rel_position)
    if dummy_distance < distance:
        closest_inverse_pose = get_pose(dummy_id, -1)
        distance = dummy_distance

    empty_position = [0, 0, -0.03, 0, 0, 0]
    empty_position[1] -= shift

    set_pose(dummy_id, object_id, empty_position)
    dummy_rel_position = get_position(dummy_id, ref_id)
    dummy_distance = np.linalg.norm(dummy_rel_position)
    if dummy_distance < distance:
        closest_inverse_pose = get_pose(dummy_id, -1)
        distance = dummy_distance

    return closest_inverse_pose


# 技能
def open_door():
    if ObjectStatus.find('cup_type') == -1:
        print('open_door something wrong!!!')
    elif ObjectStatus.find('cup_type') == 0:
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 2, vrep.simx_opmode_oneshot_wait)
        time.sleep(12)
        ObjectStatus.change('door_type', 1)
    else:
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 22, vrep.simx_opmode_oneshot_wait)
        time.sleep(12)
        ObjectStatus.change('door_type', 1)


# 技能 pour_coffee
def pour():
    vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 4, vrep.simx_opmode_oneshot_wait)
    time.sleep(35)
    ObjectStatus.change('cup_type', 1)
    time.sleep(5)
    ObjectStatus.change('door_type', 0)


# 技能 grasp_cup
def grasp(object_id):
    if object_id == IDList.find('cup_0'):  # 'cup0_id'
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 3, vrep.simx_opmode_oneshot_wait)
        time.sleep(23)
        ObjectStatus.change('rh_have_cup_type', 1)
    elif object_id == IDList.find('Fake_cup'):  # 'cup_id'
        vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'armCommand', 33, vrep.simx_opmode_oneshot_wait)
        time.sleep(20)
        ObjectStatus.change('lh_have_pot_type', 1)
    else:
        print("something wrong!!")


def open_gripper():
    vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'gripperCommand', 1, vrep.simx_opmode_oneshot_wait)


def close_gripper():
    vrep.simxSetIntegerSignal(IDList.clientID.mainID, b'gripperCommand', 0, vrep.simx_opmode_oneshot_wait)


# 技能 move_close_to_object
def move_to(object_id, type='cube'):
    object_id = int(object_id)
    ObjectStatus.change('search_type', 0)
    print('moving close to object', object_id)
    cip = get_closest_inverse_pose(object_id, IDList.find('newbot_vehicleTargetPosition'), type)
    set_pose(IDList.find('newbot_vehicleTargetPosition'), -1, cip)


# 技能 move_close_to_and_search
def move_and_search(object_id, task_name, type='cube'):
    object_id = int(object_id)
    ObjectStatus.change('search_type', 1)
    print('moving close to object', object_id)
    cip = get_closest_inverse_pose(object_id, IDList.find('newbot_vehicleTargetPosition'), type)
    set_pose(IDList.find('newbot_vehicleTargetPosition'), -1, cip)

    # keyi zengjia shexiangtou de guanjie kongzhi
    if task_name == 'MASTable':
        ObjectStatus.change('searching_type', 1)
        time.sleep(5)
        ObjectStatus.change('searching_type', 0)
        ObjectStatus.change('search_table_type', 1)
    elif task_name == 'MASRack':
        time.sleep(5)
        ObjectStatus.change('searching_type', 1)
        time.sleep(5)
        ObjectStatus.change('searching_type', 0)
        ObjectStatus.change('search_rack_type', 1)
    elif task_name == 'MASTForCoffee':
        time.sleep(15)
        ObjectStatus.change('searching_type', 1)
        time.sleep(5)
        ObjectStatus.change('searching_type', 0)
        ObjectStatus.change('st_for_coffee_type', 1)
    # elif task_name == 'MASRForCoffee':
    #     time.sleep(10)
    #     ObjectStatus.sr_for_coffee_type = 1


# 条件 is_robot_close_2d
def is_robot_close_to(object_id, threshold=0.1):
    # print('success?', object_id)
    # print('type', type(object_id).__name__)
    object_id = int(object_id)
    # print('type', type(object_id))
    position = get_position(object_id, IDList.find('newbot_reference'))
    return np.linalg.norm(position) < threshold


# 好像没用
def are_objects_close(object_1_id, object_2_id, threshold):
    position = get_position(object_1_id, object_2_id)
    return np.linalg.norm(position) < threshold


# 条件  are_objects_close2d
def is_object_at(object_1_id, object_2_id, threshold=0.12):
    object_1_id = int(object_1_id)
    object_2_id = int(object_2_id)
    # 不知道有啥用，先注释看看会不会有影响
    # VrepAPI.current_object_goal_id = object_2_id
    # VrepAPI.current_object_to_move_to_goal = object_1_id
    position = get_position(object_1_id, object_2_id)
    position[1] = position[1] - 0.1

    return np.linalg.norm(position) < threshold


# 条件 新增
def type_ok(object_name):
    name_list = [
        {'CoffeeCup': 'cup_type'}, {'OpenDoor': 'door_type'}, {'LhHavePot': 'lh_have_pot_type'},
        {'RhHaveCup': 'rh_have_cup_type'}, {'PathFree': 'path_free_type'}, {'SearchTable': 'search_table_type'},
        {'SearchRack': 'search_rack_type'}, {'STForCoffee': 'st_for_coffee_type'},
        {'SRForCoffee': 'sr_for_coffee_type'}
    ]
    for item in name_list:
        if object_name in item:
            return ObjectStatus.find(item.get(object_name)) == 1

    return False


# 条件 新增
def delivery_object(location_id, object_id, object_name):
    print('delivery_object')
    return is_object_at(object_id, location_id, 1) and type_ok(object_name)

