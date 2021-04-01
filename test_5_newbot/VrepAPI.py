try:
    import vrep
except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

import numpy as np

import time

from ObjectStatus import ObjectStatus
from IDList import IDList
from IDList import clientID


class VrepAPI:
    # vrep_api就是跟vrep的通讯，获取所有所需物体的ID来操作
    def __init__(self):
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = vrep.simxStart(b'127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP
        clientID.mainID = self.clientID
        if self.clientID != -1:
            print('Connected to remote API server')
        else:
            print('Failed connecting to remote API server')


        # self.newbot_vehicle_target_id = get_id(b'newbot_vehicleTargetPosition')
        # self.newbot_ref_id = get_id(b'newbot_reference')
        # self.right_gripper_id = get_id(b'Jaco_target')
        # self.table_id = get_id(b'Fake_table')
        # self.cup_id = get_id(b'Fake_cup')
        #
        # self.goal_id = get_id(b'goalLocation')
        # self.cup0_id = get_id(b'cup_0')
        # self.front_door_id = get_id(b'Fake_front_door')
        # self.behind_door_id = get_id(b'Fake_behind_door')
        #
        # self.current_object_goal_id = None
        # self.current_object_to_move_to_goal = None
        #
        # IDList.newbot_vehicle_target_id = self.newbot_vehicle_target_id
        # IDList.newbot_ref_id = self.newbot_ref_id
        # IDList.right_gripper_id = self.right_gripper_id
        # IDList.table_id = self.table_id
        # IDList.cup_id = self.cup_id
        # IDList.goal_id = self.goal_id
        # IDList.cup0_id = self.cup0_id
        # IDList.front_door_id = self.front_door_id
        # IDList.behind_door_id = self.behind_door_id



