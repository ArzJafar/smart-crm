import csv
from hashlib import sha256

def vk (val):
    x = list(pass_list.items())
    for i in x:
        key, value = i
        if val == value:
            print ('%10s password is: %6s ' % (name, key))

 
print('Hacking...')
print('Making hash list...')
pass_list = {}
for i in range(100000, 10000000):
    pass_list[i] = sha256(str(i).encode('utf-8')).hexdigest()
print('Hash list created!')
print('---------------')
with open('D:\Pro\py\Ex\hash_data.csv') as file:
    readit = csv.reader(file)
    next(readit)
    for i in readit:
        name, password = i
        if password in pass_list.values():
            vk(password)

print('---------------')
print('Hacked! Done!')
