import vrep
import numpy as np
import time
import ObjectStatus
import IDList


class FunctionList:
    function_list = [
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
    ]


# 下面部分要传入object_id，是某个场景下获取信息的方式，应该从场景中传入
# 动作节点呢？机器人放入当前场景必然要调试，所以这些应该是在调试过程中加入的
def get_id(client_id, name):
    error_id, target_id = vrep.simxGetObjectHandle(client_id, name, vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! id:', name, ' is not in the scene', ' and errorID:', error_id)
    else:
        return target_id


# 获取位置
def get_position(client_id, object_id, relative_id):
    error_id, position = vrep.simxGetObjectPosition(client_id, object_id, relative_id,
                                                    vrep.simx_opmode_oneshot_wait)

    if error_id:
        # raise Exception('Error! cannot retrive pose of' ,object_id)
        return [0, 0, 0]
    else:
        return position


# 获取方向
def get_orientation(client_id, object_id, relative_id):
    error_id, orientation = vrep.simxGetObjectOrientation(client_id, object_id, relative_id,
                                                          vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot retrive position of', object_id, ' and errorID:', error_id)
    else:
        return orientation


def set_position(client_id, object_id, relative_id, position):
    error_id = vrep.simxSetObjectPosition(client_id, object_id, relative_id, position,
                                          vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot set position of', object_id, ' and errorID:', error_id)


def set_orientation(client_id, object_id, relative_id, orientation):
    error_id = vrep.simxSetObjectOrientation(client_id, object_id, relative_id, orientation,
                                             vrep.simx_opmode_oneshot_wait)

    if error_id:
        raise Exception('Error! cannot set orientation of', object_id, ' and errorID:', error_id)


# 位置加方向
def get_pose(object_id, relative_id):
    return get_position(object_id, relative_id) + get_orientation(object_id, relative_id)


def set_pose(object_id, relative_id, pose):
    set_position(object_id, relative_id, pose[0:3])
    set_orientation(object_id, relative_id, pose[3:6])


def close_connection(client_id):
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
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
def open_door(client_id):
    if ObjectStatus.cup_type == 0:
        vrep.simxSetIntegerSignal(client_id, b'armCommand', 2, vrep.simx_opmode_oneshot_wait)
        time.sleep(12)
        ObjectStatus.door_type = 1
    else:
        vrep.simxSetIntegerSignal(client_id, b'armCommand', 22, vrep.simx_opmode_oneshot_wait)
        time.sleep(12)
        ObjectStatus.door_type = 1


# 技能
def pour_coffee(client_id):
    vrep.simxSetIntegerSignal(client_id, b'armCommand', 4, vrep.simx_opmode_oneshot_wait)
    time.sleep(35)
    ObjectStatus.cup_type = 1
    time.sleep(5)
    ObjectStatus.door_type = 0


# 技能
def grasp_cup(client_id, object_id):
    if object_id == 'cup0_id':
        vrep.simxSetIntegerSignal(client_id, b'armCommand', 3, vrep.simx_opmode_oneshot_wait)
        time.sleep(23)
        ObjectStatus.rh_have_cup_type = 1
    elif object_id == 'cup_id':
        vrep.simxSetIntegerSignal(client_id, b'armCommand', 33, vrep.simx_opmode_oneshot_wait)
        time.sleep(20)
        ObjectStatus.lh_have_pot_type = 1
    else:
        print("something wrong!!")


def open_gripper(client_id):
    vrep.simxSetIntegerSignal(client_id, b'gripperCommand', 1, vrep.simx_opmode_oneshot_wait)


def close_gripper(client_id):
    vrep.simxSetIntegerSignal(client_id, b'gripperCommand', 0, vrep.simx_opmode_oneshot_wait)


# 技能
# wait to correct
def move_close_to_object(object_id, type='cube'):
    ObjectStatus.search_type = 0
    print('moving close to object', object_id)
    cip = get_closest_inverse_pose(object_id, IDList.newbot_vehicle_target_id, type)
    set_pose(IDList.newbot_vehicle_target_id, -1, cip)


# 技能
def move_close_to_and_search(object_id, task_name, type='cube'):
    ObjectStatus.search_type = 1
    print('moving close to object', object_id)
    cip = get_closest_inverse_pose(object_id, IDList.newbot_vehicle_target_id, type)
    set_pose(IDList.newbot_vehicle_target_id, -1, cip)

    # keyi zengjia shexiangtou de guanjie kongzhi
    if task_name == 'MASTable':
        ObjectStatus.searching_type = 1
        time.sleep(5)
        ObjectStatus.searching_type = 0
        ObjectStatus.search_table_type = 1
    elif task_name == 'MASRack':
        time.sleep(5)
        ObjectStatus.searching_type = 1
        time.sleep(5)
        ObjectStatus.searching_type = 0
        ObjectStatus.search_rack_type = 1
    elif task_name == 'MASTForCoffee':
        time.sleep(15)
        ObjectStatus.searching_type = 1
        time.sleep(5)
        ObjectStatus.searching_type = 0
        ObjectStatus.st_for_coffee_type = 1
    # elif task_name == 'MASRForCoffee':
    #     time.sleep(10)
    #     ObjectStatus.sr_for_coffee_type = 1


# 条件
def is_robot_close_2d(object_id, threshold):
    position = get_position(object_id, IDList.newbot_ref_id)
    return np.linalg.norm(position) < threshold


def are_objects_close(object_1_id, object_2_id, threshold):
    position = get_position(object_1_id, object_2_id)
    return np.linalg.norm(position) < threshold


# 条件
def are_objects_close2d(object_1_id, object_2_id, threshold):
    # 不知道有啥用，先注释看看会不会有影响
    # VrepAPI.current_object_goal_id = object_2_id
    # VrepAPI.current_object_to_move_to_goal = object_1_id
    position = get_position(object_1_id, object_2_id)
    position[1] = position[1] - 0.1

    return np.linalg.norm(position) < threshold
