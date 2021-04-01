class IDList:
    id_list = [{'name': 'newbot_vehicleTargetPosition', 'value': None},
               {'name': 'newbot_reference', 'value': None},
               {'name': 'Jaco_target', 'value': None},
               {'name': 'Fake_table', 'value': None},
               {'name': 'Fake_cup', 'value': None},
               {'name': 'goalLocation', 'value': None},
               {'name': 'cup_0', 'value': None},
               {'name': 'Fake_front_door', 'value': None},
               {'name': 'Fake_behind_door', 'value': None},
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

