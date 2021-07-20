# Author / Maintainer : Rejoy Roy Mathews

class Memory(object):
    '''Generic Memory Model that takes allows initializing a memory with depth > 0.
    If an initial value is defined, the Memory initializes all the addresses
    with the intial value
    '''
    def __init__(self, name : str = 'default', depth : int = 0, init_value = 'X') -> None:
        
        self._memory_data_struct = {}
        self._depth = depth
        self._name = name
        self._memory_writes = 0
        self._memory_reads = 0

        if depth > 0 and init_value:
            for addr in range(depth):
                self._memory_data_struct[addr] = init_value


    def memory_write(self, addr : int, data : int) -> None:
        '''Memory Write Operation : Memory[addr] = data'''
        if self._depth > 0:
            if addr >= self._depth:
                raise IndexError(f'Memory {self._name} : Out of range write to addr={addr}')

        self._memory_writes+=1
        self._memory_data_struct[addr] = data


    def memory_read(self, addr : int) -> int:
        '''Memory read operation : returns Memory[addr]'''
        try:         
            self._memory_data_struct[addr]
        except KeyError:
            print(f'Memory {self._name} : Out of range read addr={addr}')
        else:
            self._memory_reads+=1
            return self._memory_data_struct[addr]            

    @property
    def name(self) -> str:
        '''Defines the memory name'''
        return self._name

    def __str__(self) -> str:
        out_str = ''
        out_str = out_str + '=================='+'='*len(self._name) +'\n'       
        out_str = out_str + f'Memory {self._name} contents. \n'
        out_str = out_str + '=================='+'='*len(self._name) +'\n'
        for k,v in self._memory_data_struct.items():            
            out_str = out_str + f'addr[{k}] : {v}.\n'

        return out_str

    def stats(self) -> None:
        '''Displays the total number of memory read and write acceses'''
        out_str = ''
        out_str = out_str + f'Memory {self._name} total reads : {self._memory_reads} \n'
        out_str = out_str + f'Memory {self._name} total writes : {self._memory_writes} \n'
        print(out_str)