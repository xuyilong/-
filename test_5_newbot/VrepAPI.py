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



