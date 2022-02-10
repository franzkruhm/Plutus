#################################################################################
## SCROO database loader: a multithreaded, memcached, keygen fixed Plutus fork ##
## by Franz Kruhm                                                              ##
#################################################################################
## This implements use of memcached to allow sharing of the database between   ##
## threads. With the current pickled database of 15th march 2021 the RAM use   ##
## is about 4100gigs for memcached database.                                   ##
##                                                                             ##
## The keygen in Plutus has been rewritten as it was returning erroneous       ##
## addresses.                                                                  ##
##                                                                             ##
## The GPL3 applies.                                                           ##
##                                                                             ##
#################################################################################
## This loads the text file containing the addresses into memcached and        ##
## randomly selects sanity check values while loading                          ##
#################################################################################

import random
import os
from pymemcache.client import base
from datetime import datetime
import time

DATABASE_PATH = r'database/data.txt'

sanity_1_i = random.randint(0, 34000000)
sanity_2_i = random.randint(0, 34000000)
sanity_1_s = ''
sanity_1_s = ''

print('connect memcached...')
client = base.Client(('localhost', 11211))
print('Loading and injecting database')
print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
startTime = time.time()

i_add = 0
f = open(DATABASE_PATH, 'r')
while True:
    alist = []
    lines = f.readlines(32768)
    if not lines:
        break
    for i in lines:
        alist.append(i.rstrip('\n'))
        i_add += 1
        if i_add == sanity_1_i:
            sanity_1_s = i.rstrip('\n')
        if i_add == sanity_2_i:
            sanity_2_s = i.rstrip('\n')
    client.set_multi(dict.fromkeys(alist, 1), expire=0)
    #client.set(line, '1', expire = 0) 
    print('\raddresses: ' + str(i_add), end=' ')

f.close()
endTime = time.time()
executionTime = (endTime - startTime)
print('DONE LOADING DATABASE: Addresses loadeded in ' + str(round(executionTime, 2)) + ' seconds!')
print('sanity 1: ' + sanity_1_s + ' sanity 2: ' + sanity_2_s)

print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
ret = False
ret = client.get(sanity_1_s)
if ret:
    print('sanity check pass')
else:
    print('check failed:1')
    quit()
ret = False
ret = client.get(sanity_2_s)
if ret:
    print('sanity check pass')
else:
    print('check failed:2')
    quit()

f = open('sanity.txt', 'w')
f.write(sanity_1_s + '\n')
f.write(sanity_2_s + '\n')
f.close()
