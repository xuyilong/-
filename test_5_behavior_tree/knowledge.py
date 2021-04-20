# 后期这部分知识会从知识图谱中获得
def find_from_know(node):
    sublist = []
    if node.name == 'path_free':
        if node.location_id == '497':
            sublist = [{'name': 'is_robot_close_to', 'parm': {'location_id': '495'}},
                       {'name': 'is_open', 'parm': {'door_id': '495'}},
                       {'name': 'move_to', 'parm': {'door_id': '496'}}, ]
        if node.location_id == '478':
            sublist = [{'name': 'is_robot_close_to', 'parm': {'location_id': '496'}},
                       {'name': 'is_open', 'parm': {'door_id': '496'}},
                       {'name': 'move_to', 'parm': {'door_id': '495'}}, ]
    if node.name == 'is_ready':
        if node.object_id == '497' and node.object_name == 'coffee':
            sublist = [{'name': 'is_hold', 'parm': {'object_id': '474', 'hand_id': '459'}},
                       {'name': 'is_hold', 'parm': {'object_id': '497', 'hand_id': '356'}},
                       {'name': 'pour_coffee', 'parm': {'object_id_1': '497', 'object_id_2': '474'}}, ]

    return sublist
