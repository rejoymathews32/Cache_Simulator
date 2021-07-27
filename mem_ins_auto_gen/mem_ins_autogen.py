import os
#from random import randrange, random
import random
from random import randrange
 
curr_dir = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(curr_dir, 'autogen_ins.txt')
trans_type = ['W', 'R']
with open(filepath,'w') as fp:
    for x in range(32768):
        trans_sel = random.choice(trans_type)
        addr = hex(randrange(16384))
        if(trans_sel == 'W'):
            data = addr
            fp.write(f'{trans_sel} {addr} {data}\n')
        else:
            fp.write(f'{trans_sel} {addr}\n')
fp.close()

