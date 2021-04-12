class ObjectStatus:
    status_list = [{'name': 'cup_type', 'status': 0},
                   {'name': 'door_type', 'status': 0},
                   {'name': 'lh_have_pot_type', 'status': 0},
                   {'name': 'rh_have_cup_type', 'status': 0},
                   {'name': 'path_free_type', 'status': 1},
                   {'name': 'search_table_type', 'status': 0},
                   {'name': 'search_rack_type', 'status': 0},
                   {'name': 'st_for_coffee_type', 'status': 0},
                   {'name': 'sr_for_coffee_type', 'status': 0},
                   {'name': 'searching_type', 'status': 0},  # 标记是否正在search
                   {'name': 'search_type', 'status': 0},  # 主要标记是move还是move_and_search，这里很可能用不到
                   ]


def find(name):
    for item in ObjectStatus.status_list:
        if item.get('name') == name:
            return item.get('status')
    return -1


def change(name, status):
    for item in ObjectStatus.status_list:
        if item.get('name') == name:
            item['status'] = status
            return
    return


def add_status(name, status):
    ObjectStatus.status_list.append({'name': name, 'status': status})


def show_status_list():
    num = len(ObjectStatus.status_list)
    print('Now we have %s object(s)' % num)
    print('They are:', ObjectStatus.status_list)
