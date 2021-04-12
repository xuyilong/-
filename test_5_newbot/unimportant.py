import ObjectStatus


def wd():
    print(1 == 1)
    print('do what')
    return 1 == 1


if __name__ == '__main__':
    flag = wd()
    print(flag)


# 仿真开始与停止
# print('发生了什么吗')
# vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
# vrep.simxStopSimulation(clientID, vrep.simx_opmode_oneshot)
# vrep.simxPauseSimulation(clientID, vrep.simx_opmode_oneshot)
# print('完成')