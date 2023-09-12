import json

arr = []

with open('censorship.txt', 'r',  encoding='cp1251') as r:
    for i in r:
        string = i.lower().split('\n')[0]
        if string != '':
            arr.append(string)

with open('censorship.json', 'w', encoding='cp1251') as w:
    json.dump(arr, w)
