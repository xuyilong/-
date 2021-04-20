import ObjectStatus


def wd():
    ObjectStatus.add_status('xu', 10)
    new_list = ObjectStatus.ObjectStatus.status_list
    for i in new_list:
        if i.get('name') == 'xu':
            print('wozhongla')
        print(i)
    print('do what')
    return 1 == 1


def aa():
    dic1 = {'a1': 'b1', 'a2': 'b2'}
    print(dic1.get('a3'))


if __name__ == '__main__':
    aa()
    # flag = wd()
    # print(flag)


# 仿真开始与停止
# print('发生了什么吗')
# vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
# vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
# vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot)
# print('完成')
