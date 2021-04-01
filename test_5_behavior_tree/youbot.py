import sys
sys.path.insert(0, 'bt/')
from SequenceNode import SequenceNode
from FallbackNode import FallbackNode
from NewDraw import new_draw_tree
from BTSearchActionNodes import *
from BTSearchConditionNodes import *
from FailNode import FailNode
from id_list import IDList
from global_var import GlobalVar


def newbot():
    print('newbot')

    delivery_coffee = DeliveryObject('DeliveryCoffee', vrep.cup0_id, vrep.goal_id, 'CoffeeCup')

    root = FallbackNode('root')

    root.AddChild(delivery_coffee)

    draw_thread = threading.Thread(target=new_draw_tree, args=(root,))
    draw_thread.start()
    # time.sleep(10)

    while True:
        print('-------------执行前------------------')
        while True:
            root.Execute(None)
            time.sleep(1)
            if root.GetStatus() == 1:
                break

        print('-------------执行后-----------------')

        if FailNode.failChildNode is None:
            continue
        childNode = FailNode.failChildNode
        fatherNode = FailNode.failFatherNode
        childAddress = FailNode.address

        # 要找到它自己的根 暂不考虑冲突
        # subTree = expandTree(childNode)
        subTree = new_expand_tree(childNode)
        fatherNode.RemoveChild(childNode)
        fatherNode.AddChild(subTree, childAddress)


def xian():
    time.sleep(10)
    skill_list = []
    tem_xian = 0
    tem_wheel = 0
    while True:
        arm_error_id, arm_command = v.simxGetIntegerSignal(0, b'armCommand', v.simx_opmode_streaming)
        if arm_command != 0 and arm_command != 1 and arm_command != 11 and arm_command != tem_xian:
            tem_xian = arm_command
            if arm_command == 2:
                tem_skill = {'Name': 'BothHandsOpenDoor',
                             'Behavior': ['RaiseBothArms', 'StretchBothArms', 'PushDoor', 'HoldInitialStatus']}
                skill_list.append(tem_skill)
            if arm_command == 3:
                tem_skill = {'Name': 'RightHandGraspCup',
                             'Behavior': ['RaiseRightArm', 'RaiseRightForearm',
                                          'AdjustRightArm', 'CloseToGoal', 'GraspObject', 'KeepPickUp']}
                skill_list.append(tem_skill)
            if arm_command == 22:
                tem_skill = {'Name': 'LeftHandOpenDoor',
                             'Behavior': ['RaiseLeftArm', 'StretchLeftArm', 'PushDoor', 'HoldInitialStatus']}
                skill_list.append(tem_skill)
            if arm_command == 33:
                tem_skill = {'Name': 'LeftHandGraspCup',
                             'Behavior': ['RaiseLeftArm', 'StretchLeftArm', 'GraspObject', 'KeepPickUp']}
                skill_list.append(tem_skill)
            if arm_command == 4:
                tem_skill = {'Name': 'PourCoffee',
                             'Behavior': ['AustLeftArmHeight', 'RightHandClose', 'LeftHandPour', 'RecoverLeftHand',
                                          'OpenLeftGripper', 'RaiseLeftForearm', 'RaiseLeftArm', 'PutDownLeftForearm',
                                          'PutDownLeftArm', 'KeepPickUp']}
                skill_list.append(tem_skill)

        wheel_error_id, wheel = v.simxGetIntegerSignal(0, b'wheel', v.simx_opmode_streaming)
        if tem_wheel != wheel and wheel == 1:
            if ObjectStatus.search_type == 0:
                tem_skill = {'Name': 'Move', 'Behavior': ['MoveToGoal']}
                skill_list.append(tem_skill)
            if ObjectStatus.search_type == 1:
                tem_skill = {'Name': 'MoveAndSearch', 'Behavior': ['MoveToGoal', 'Search']}
                skill_list.append(tem_skill)
        tem_wheel = wheel

        behavior_error_id, behavior_name = v.simxGetIntegerSignal(0, b'behaviorName', v.simx_opmode_streaming)
        if wheel == 1:
            behavior_name = 1
        if ObjectStatus.searching_type > 0:
            behavior_name = 2

        # 先不输出节点的运行顺序
        # pint(skill_list)
        # if behavior_name > 0:
        #     print('Now running node:', skill_list[len(skill_list)-1]['Behavior'][behavior_name-1])
        # else:
        #     print('Now no node running')
        time.sleep(0.5)


# 暂写，不一定正确
def new_expand_tree(node):
    print('newExpandTree')
    subtree = FallbackNode('Fallback')
    subtree.AddChild(node)
    for item in GlobalVar.subtree_list:
        if item.get('post_condition') == node:
            sequence = SequenceNode('Sequence')
            pre_condition_list = item.get('pre_condition_list')
            for i in pre_condition_list:
                sequence.AddChild(SubConditionNode(**i))
            skill = SubActionNode(**item.get('skill'))
            sequence.AddChild(skill)
    return subtree


def expandTree(node):
    print("expandTree")

    if node.name == 'DeliveryCoffee':
        delivery_coffee_subtree = FallbackNode('DeliveryCoffeeFallback')

        delivery_coffee_subtree.AddChild(node)

        delivery_coffee_sequence = SequenceNode('DeliveryCoffeeSequence')

        goal_id = node.at
        robot_have_coffee = TypeOK('RobotHaveCoffee', 'CoffeeCup')
        could_move_to_goal = TypeOK('IsDoorBOpen', 'OpenDoor')
        move_to_goal = MoveCloseTo('MoveCloseToGoal', goal_id)

        delivery_coffee_sequence.AddChild(robot_have_coffee)
        delivery_coffee_sequence.AddChild(could_move_to_goal)
        delivery_coffee_sequence.AddChild(move_to_goal)

        delivery_coffee_subtree.AddChild(delivery_coffee_sequence)

        return delivery_coffee_subtree

    elif node.name == 'RobotHaveCoffee':
        robot_have_coffee_subtree = FallbackNode('RobotHaveCoffeeFallback')

        robot_have_coffee_subtree.AddChild(node)

        robot_have_coffee_sequence = SequenceNode('RobotHaveCoffeeSequence')

        found_coffee = TypeOK('IsCoffeeReady', 'CoffeeCup')
        is_close_to_cup0 = IsRobotCloseTo('IsRobotCloseToCup', IDList.cup0_id)
        grasp_cup = GraspCup('GraspCup', 'cup0_id')

        robot_have_coffee_sequence.AddChild(found_coffee)
        robot_have_coffee_sequence.AddChild(is_close_to_cup0)
        robot_have_coffee_sequence.AddChild(grasp_cup)

        robot_have_coffee_subtree.AddChild(robot_have_coffee_sequence)

        return robot_have_coffee_subtree

    elif node.name == 'IsCoffeeReady':
        found_coffee_subtree = FallbackNode('FoundCoffeeFallback')

        found_coffee_subtree.AddChild(node)

        found_coffee_sequence = SequenceNode('FoundCoffeeSequence')

        # keyi zengjia OpenDoor de panduan tiaojian
        could_move_to_room = TypeOK('IsDoorFOpen', 'OpenDoor')
        table_has_searched_for_coffee = TypeOK('HasSearchedTable', 'STForCoffee')
        make_coffee = TypeOK('MadeCoffee', 'CoffeeCup')

        found_coffee_sequence.AddChild(could_move_to_room)
        found_coffee_sequence.AddChild(table_has_searched_for_coffee)
        found_coffee_sequence.AddChild(make_coffee)

        found_coffee_subtree.AddChild(found_coffee_sequence)

        return found_coffee_subtree

    elif node.name == 'IsDoorFOpen':
        could_move_to_room_subtree = FallbackNode('CouldMoveToRoomFallback')

        could_move_to_room_subtree.AddChild(node)

        could_move_to_room_sequence = SequenceNode('CouldMoveToRoomSequence')

        is_close_to_door = IsRobotCloseTo('IsRobotCloseToFDoor', IDList.front_door_id)
        open_door = OpenDoor('OpenDoor')

        could_move_to_room_sequence.AddChild(is_close_to_door)
        could_move_to_room_sequence.AddChild(open_door)

        could_move_to_room_subtree.AddChild(could_move_to_room_sequence)

        return could_move_to_room_subtree

    elif node.name == 'IsRobotCloseToFDoor':
        is_robot_close_to_fdoor_subtree = FallbackNode('IsRobotCloseToFDoorFallback')

        is_robot_close_to_fdoor_subtree.AddChild(node)

        is_robot_close_to_fdoor_sequence = SequenceNode('IsRobotCloseToFDoorSequence')

        path_free = TypeOK('PathFree', 'PathFree')
        move_to_door = MoveCloseTo('MoveCloseToFDoor', IDList.front_door_id)

        is_robot_close_to_fdoor_sequence.AddChild(path_free)
        is_robot_close_to_fdoor_sequence.AddChild(move_to_door)

        is_robot_close_to_fdoor_subtree.AddChild(is_robot_close_to_fdoor_sequence)

        return is_robot_close_to_fdoor_subtree

    elif node.name == 'HasSearchedTable':
        table_has_searched_coffee_subtree = FallbackNode('TableHasSearchedCoffeeFallback')

        table_has_searched_coffee_subtree.AddChild(node)

        table_has_searched_coffee_sequence = SequenceNode('TableHasSearchedCoffeeSequence')

        path_free = TypeOK('PathFree', 'PathFree')
        move_and_search_to_table = MoveCloseToAndSearch('MoveAndSearchTable', IDList.table_id, 'MASTForCoffee')

        table_has_searched_coffee_sequence.AddChild(path_free)
        table_has_searched_coffee_sequence.AddChild(move_and_search_to_table)

        table_has_searched_coffee_subtree.AddChild(table_has_searched_coffee_sequence)

        return table_has_searched_coffee_subtree

    elif node.name == 'MadeCoffee':
        made_coffee_subtree = FallbackNode('MadeCoffeeFallback')

        made_coffee_subtree.AddChild(node)

        made_coffee_sequence = SequenceNode('MadeCoffeeSequence')

        lh_have_pot = TypeOK('LeftHandHavePot', 'LhHavePot')
        rh_have_cup = TypeOK('RightHandHaveCup', 'RhHaveCup')
        pour_coffee = PourTo('PourCoffee')

        made_coffee_sequence.AddChild(lh_have_pot)
        made_coffee_sequence.AddChild(rh_have_cup)
        made_coffee_sequence.AddChild(pour_coffee)

        made_coffee_subtree.AddChild(made_coffee_sequence)

        return made_coffee_subtree

    elif node.name == 'LeftHandHavePot':
        lh_have_pot_subtree = FallbackNode('LhHaveCupFallback')

        lh_have_pot_subtree.AddChild(node)

        lh_have_pot_sequence = SequenceNode('LhHavePotSequence')

        is_close_to_cup = IsRobotCloseTo('IsRobotCloseToPot', IDList.cup_id)
        grasp_cup = GraspCup('GraspCup', 'cup_id')

        lh_have_pot_sequence.AddChild(is_close_to_cup)
        lh_have_pot_sequence.AddChild(grasp_cup)

        lh_have_pot_subtree.AddChild(lh_have_pot_sequence)

        return lh_have_pot_subtree

    elif node.name == 'IsRobotCloseToPot':
        is_close_to_pot_subtree = FallbackNode('IsCloseToCupFallback')

        is_close_to_pot_subtree.AddChild(node)

        is_close_to_pot_sequence = SequenceNode('IsCloseToPotSequence')

        could_move_to_pot = TypeOK('CouldMoveToPot', 'SearchRack')
        move_to_pot = MoveCloseTo('MoveAndSearchTable', IDList.cup_id)

        is_close_to_pot_sequence.AddChild(could_move_to_pot)
        is_close_to_pot_sequence.AddChild(move_to_pot)

        is_close_to_pot_subtree.AddChild(is_close_to_pot_sequence)

        return is_close_to_pot_subtree

    elif node.name == 'CouldMoveToPot':
        could_move_to_pot_subtree = FallbackNode('CouldMoveToPotFallback')

        could_move_to_pot_subtree.AddChild(node)

        could_move_to_pot_sequence = SequenceNode('CouldMoveToPotSequence')

        table_has_searched = TypeOK('TableHasSearched', 'SearchTable')
        rack_has_searched = TypeOK('RackHasSearched', 'SearchRack')

        could_move_to_pot_sequence.AddChild(table_has_searched)
        could_move_to_pot_sequence.AddChild(rack_has_searched)

        could_move_to_pot_subtree.AddChild(could_move_to_pot_sequence)

        return could_move_to_pot_subtree

    elif node.name == 'TableHasSearched':
        table_has_searched_subtree = FallbackNode('TableHasSearchedFallback')

        table_has_searched_subtree.AddChild(node)

        table_has_searched_sequence = SequenceNode('TableHasSearchedSequence')

        path_free = TypeOK('PathFree', 'PathFree')
        move_and_search_to_table = MoveCloseToAndSearch('MoveAndSearchTable', IDList.table_id, 'MASTable')

        table_has_searched_sequence.AddChild(path_free)
        table_has_searched_sequence.AddChild(move_and_search_to_table)

        table_has_searched_subtree.AddChild(table_has_searched_sequence)

        return table_has_searched_subtree

    elif node.name == 'RackHasSearched':
        rack_has_searched_subtree = FallbackNode('RackHasSearchedFallback')

        rack_has_searched_subtree.AddChild(node)

        rack_has_searched_sequence = SequenceNode('RackHasSearchedSequence')

        path_free = TypeOK('PathFree', 'PathFree')
        move_and_search_to_rack = MoveCloseToAndSearch('MoveAndSearchRack', IDList.cup_id, 'MASRack')

        rack_has_searched_sequence.AddChild(path_free)
        rack_has_searched_sequence.AddChild(move_and_search_to_rack)

        rack_has_searched_subtree.AddChild(rack_has_searched_sequence)

        return rack_has_searched_subtree

    elif node.name == 'RightHandHaveCup':
        rh_have_cup0_subtree = FallbackNode('RhHaveCup0Fallback')

        rh_have_cup0_subtree.AddChild(node)

        rh_have_cup0_sequence = SequenceNode('LhHaveCup0Sequence')

        is_close_to_cup0 = IsRobotCloseTo('IsRobotCloseToCup', IDList.cup0_id)
        grasp_cup = GraspCup('GraspCup', 'cup0_id')

        rh_have_cup0_sequence.AddChild(is_close_to_cup0)
        rh_have_cup0_sequence.AddChild(grasp_cup)

        rh_have_cup0_subtree.AddChild(rh_have_cup0_sequence)

        return rh_have_cup0_subtree

    elif node.name == 'IsRobotCloseToCup':
        is_close_to_cup_subtree = FallbackNode('IsCloseToCupFallback')

        is_close_to_cup_subtree.AddChild(node)

        is_close_to_cup_sequence = SequenceNode('IsCloseToCupSequence')

        could_move_to_cup = TypeOK('CouldMoveToCup', 'PathFree')
        move_to_cup = MoveCloseTo('MoveCloseToCup', IDList.table_id)

        is_close_to_cup_sequence.AddChild(could_move_to_cup)
        is_close_to_cup_sequence.AddChild(move_to_cup)

        is_close_to_cup_subtree.AddChild(is_close_to_cup_sequence)

        return is_close_to_cup_subtree

    elif node.name == 'IsDoorBOpen':
        could_move_to_goal_subtree = FallbackNode('CouldMoveToGoalFallback')

        could_move_to_goal_subtree.AddChild(node)

        could_move_to_goal_sequence = SequenceNode('CouldMoveToGoalSequence')

        is_close_to_door = IsRobotCloseTo('IsRobotCloseToBDoor', IDList.behind_door_id)
        open_door = OpenDoor('OpenDoor')

        could_move_to_goal_sequence.AddChild(is_close_to_door)
        could_move_to_goal_sequence.AddChild(open_door)

        could_move_to_goal_subtree.AddChild(could_move_to_goal_sequence)

        return could_move_to_goal_subtree

    elif node.name == 'IsRobotCloseToBDoor':
        is_robot_close_to_bdoor_subtree = FallbackNode('IsRobotCloseToFDoorFallback')

        is_robot_close_to_bdoor_subtree.AddChild(node)

        is_robot_close_to_bdoor_sequence = SequenceNode('IsRobotCloseToFDoorSequence')

        path_free = TypeOK('PathFree', 'PathFree')
        move_to_door = MoveCloseTo('MoveCloseToBDoor', IDList.behind_door_id)

        is_robot_close_to_bdoor_sequence.AddChild(path_free)
        is_robot_close_to_bdoor_sequence.AddChild(move_to_door)

        is_robot_close_to_bdoor_subtree.AddChild(is_robot_close_to_bdoor_sequence)

        return is_robot_close_to_bdoor_subtree


if __name__ == "__main__":
    xian_thread = threading.Thread(target=xian, args=())
    xian_thread.start()
    newbot()
