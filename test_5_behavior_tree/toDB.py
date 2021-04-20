import shelve


# 在subtreee_list.db中，我加入了一个num，作为新增数据时的一个索引，
# 但是同样在遍历list时，就会多出一个num数据，要再把它踢出来可能就多浪费了一些内存
# 这个num，可能作为索引，但不会直接显示，应该是这样


def add(sub_list):
    # ('add sub_list', sub_list)
    db = shelve.open('subtree_list.db')
    # 这个num是数字，作为标识的时候是string
    num = db.get('num')
    for item in sub_list:
        num = num + 1
        # print('item', item)
        snum = str(num)
        db[snum] = item

    # print(num)
    db['num'] = num
    db.close()


# 看看文件中都保存了什么
def look():
    db = shelve.open('subtree_list.db')
    print('items', list(db.items()))
    print(db.get('num'))
    db.close()


# 输出所有的子树
def get_all():
    db = shelve.open('subtree_list.db')
    sublist = list(db.items())
    for item in sublist:
        if item[0] == 'num':
            sublist.remove(item)
    return sublist


def delete_by_num(num):
    db = shelve.open('subtree_list.db')
    del db[str(num)]
    db.close()


def delete_all():
    db = shelve.open('subtree_list.db')
    db['num'] = 0
    print(list(db.items()))
    db.close()


# add([10, 20])
# delete()


# dic.get() 是None  dic[]会报错

# 如果删除了一个不存在的，就会报错
# del db['new'], db['aa']
# db = shelve.open('subtree_list.db')

if __name__ == '__main__':
    look()
