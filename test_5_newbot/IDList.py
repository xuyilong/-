class IDList:
    id_list = [{'name': 'newbot_vehicle_target_position', 'value': None},
               {'name': 'newbot_reference', 'value': None},
               {'name': 'left_hand', 'value': None},
               {'name': 'right_hand', 'value': None},
               {'name': 'cup_2', 'value': None},
               {'name': 'cup_1', 'value': None},
               {'name': 'door_1_f', 'value': None},
               {'name': 'door_1_b', 'value': None},
               {'name': 'location_1', 'value': None},
               ]


class clientID:
    mainID = None


def change_value(name, value):
    for item in IDList.id_list:
        if item.get('name') == name:
            item['value'] = value


def add_id(name, value):
    IDList.id_list.append({'name': name, 'value': value})


def find(name):
    for item in IDList.id_list:
        if item.get('name') == name:
            return item.get('value')
    print('find wrong')
    return -1


def show_id_list():
    num = len(IDList.id_list)
    print('Now we have %s object(s)' % num)
    print('They are:', IDList.id_list)

