from BTSearchConditionNodes import SubConditionNode
import toDB


def aa():
    a = [1, 2, 3]
    print(a)
    return a


def bb():
    b = aa()
    b.append(4)
    print('b', b)
    aa()


bb()
