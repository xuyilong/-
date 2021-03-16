class ObjectStatus:
    def __init__(self, object_status=None):
        if object_status is None:
            object_status = []
        self.object_status = object_status

    def add_status(self, name, status):
        self.object_status.append({'name': name, 'status': status})

    def show_object_status(self):
        num = len(self.object_status)
        print('Now we have %d object(s)' % num)
        print('They are:', self.object_status)

    # cup_type = 0
    # door_type = 0
    # in_room_type = 0
    # lh_have_pot_type = 0
    # rh_have_cup_type = 0
    # path_free_type = 1
    # search_table_type = 0
    # search_rack_type = 0
    # st_for_coffee_type = 0
    # sr_for_coffee_type = 0
    # searching_type = 0
    # search_type = 0
