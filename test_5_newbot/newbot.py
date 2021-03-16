from VrepAPI import *
import IDList
import FunctionList


class cid:
    cid = None


def id_add(name):
    bname = bytes(name, encoding="utf8")
    gid = FunctionList.get_id(cid.cid, bname)
    return name, gid


def newbot():
    print('newbot')
    v_rep = VrepAPI()
    cid.cid = v_rep.clientID

    id_list = IDList.IDList()
    id_name_list = ['newbot_vehicleTargetPosition',
                    'newbot_reference',
                    'Jaco_target',
                    'Fake_table',
                    'Fake_cup',
                    'goalLocation',
                    'cup_0',
                    'Fake_front_door',
                    'Fake_behind_door',
                    ]
    for item in id_name_list:
        id_list.add_id(id_add(item))

    status_list = ObjectStatus()
    status_name_list = ['cup_type',
                        'door_type',
                        'in_room_type',
                        'lh_have_pot_type',
                        'rh_have_cup_type',
                        'path_free_type',
                        'search_table_type',
                        'search_rack_type',
                        'st_for_coffee_type',
                        'sr_for_coffee_type',
                        'searching_type',
                        'search_type',
                        ]
    for item in status_name_list:
        status_list.add_status(item, 0)
    status_list.object_status[5] = 1


if __name__ == "__main__":
    newbot()
