from Memory import Memory


class Cache(object):
    '''This class models a cache'''
    def __init__(self) -> None:        
        self._Cache_Memory = Memory(32,0)

        # self._Cache_Memory.memory_write(0,23)
        # print(self._Cache_Memory.memory_read(0))
        #help(self._Cache_Memory)
        print(self._Cache_Memory)

test = Cache()
    
    
    

