class ObjectStatus:
    status_list = [{'name': 'cup_type', 'status': 0},   # 标记杯子里面有没有咖啡
                   {'name': 'door_type', 'status': 0},  # 标记门是否开了
                   {'name': 'lh_have_pot_type', 'status': 0},
                   {'name': 'rh_have_cup_type', 'status': 0},
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
