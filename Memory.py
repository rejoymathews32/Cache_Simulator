class Memory(object):
    '''This class models a memory'''
    def __init__(self, depth : int = 2, init_value = 'X') -> None:
        
        self._memory_data_struct = {}
        self._depth = depth

        for x in range(depth):
            self._memory_data_struct.update({x:init_value})


    def memory_write(self, write_address : int, write_data : hex) -> None:

        if(not(write_address >= 0 and write_address < self._depth)):
            assert IndexError('Address is out of memory range')

        self._memory_data_struct.update({hex(write_address):hex(write_data)})


    def memory_read(self, read_address : int) -> hex:

        if(not(read_address >= 0 and read_address < self._depth)):
            assert IndexError('Address is out of memory range')

        return self._memory_data_struct[read_address]

    def __str__(self) -> str:
        out_str = ''
        for k,v in self._memory_data_struct.items():            
            out_str = out_str + f'Address:{k} has a data value of {v}.\n'

        return out_str
