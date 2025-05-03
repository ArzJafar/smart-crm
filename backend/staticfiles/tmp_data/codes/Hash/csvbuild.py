import csv
from hashlib import sha256
from random import randint

names = ['Hera', 'Arz', 'Barana', 'Mmdreza', 'Rahimi', 'Ahmadian']
passha = {}
list_pass = {}

for i in names:
    adad = str(randint(100000, 999999))
    pass_hash = sha256(adad.encode('utf-8')).hexdigest()
    list_pass[i] = pass_hash
    passha[i] = adad

with open('D:\Pro\py\Ex\hash_data.csv', mode = 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['name', 'hash'])
    for k, v in list_pass.items():
        writer.writerow([k, v])
    for k,v in passha.items():
        writer.writerow([k,v])
