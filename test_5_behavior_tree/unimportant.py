def bb():
    dic1 = {'name': 'xu', 'parm': {'pp': 'xx'}}
    dic2 = [{'aa': 'bb', 'ss': {'name': 'xu', 'parm': {'pp': 'aa'}}},
            {'aa': 'bb', 'ss': {'name': 'xu', 'parm': {'pp': 'xx'}}}]
    for item in dic2:
        print(dic1 == item.get('ss'))
    for i in dic1:
        print(i, dic1[i])


bb()
