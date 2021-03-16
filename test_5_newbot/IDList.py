class IDList:
    def __init__(self, id_list=None):
        if id_list is None:
            id_list = []
        self.id_list = id_list

    def add_id(self, name, value):
        self.id_list.append({'name': name, 'value': value})

    def show_id_list(self):
        num = len(self.id_list)
        print('Now we have %s object(s)' % num)
        print('They are:', self.id_list)



    # clientID = None
    # newbot_vehicle_target_id = None
    # newbot_ref_id = None
    # right_gripper_id = None
    # table_id = None
    # cup_id = None
    # goal_id = None
    # cup0_id = None
    # front_door_id = None
    # behind_door_id = None
    # current_object_goal_id = None
    # current_object_to_move_to_goal = None
