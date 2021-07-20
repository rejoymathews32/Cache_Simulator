# Author / Maintainer : Rejoy Roy Mathews

from cache import Cache
from LRU import LRU
from Memory import Memory
import argparse

class cache_simulator(object):
    '''Class simulator takes in a user cache configuration(name, size, 
    associativity, write policy) & memory configuration(name, size)
    and simulates cache and external memory accesses for the
    cache configuration.
    The cache replacement policy used is the Least Recently Used(LRU)
    replacement policy.
    '''

    def __init__(self, cache_sim_param : dict) -> None:
        self._r_policy      = LRU()
        self._extern_memory = Memory(cache_sim_param['mem_name'],
                            cache_sim_param['mem_size'])
        self._cache         = Cache(cache_sim_param['cache_name'],
                            cache_sim_param['cache_size'],
                            cache_sim_param['cache_assoc'],
                            cache_sim_param['cache_wr_policy'],
                            self._extern_memory,
                            self._r_policy
                            )


    def run(self, cache_ops_inp) ->  None:

        with open(cache_ops_inp, 'r') as f:
            cache_ops = [line.split() for line in f]

        for ins in range(len(cache_ops)):
            if cache_ops[ins][0] == 'R':
                self._cache.read_from_cache(int(cache_ops[ins][1]))
            elif cache_ops[ins][0] == 'W':
                self._cache.write_to_cache(int(cache_ops[ins][1]), int(cache_ops[ins][2]))
            else:
                raise ValueError('Specify "R" for read operations or  \
                                "W" for write operations as the opcode for the operation')

        #RRM
        self._stats()
        self._cache_dump()
        self._extern_memory_dump()


    def _extern_memory_dump(self) -> None:
        '''Print the contents of the external memory'''
        print(self._extern_memory)

    def _cache_dump(self) -> None:
        '''Print the contents of the cache'''
        print(self._cache)

    def _stats(self) -> None:
        '''
        Print the cache hits, cache misses, cache reads, cache writes
        memory reads and memory write statistics
        '''
        self._cache.stats()
        self._extern_memory.stats()

def main():
    parser = argparse.ArgumentParser(            
             description='Run cache simulator.')
    parser.add_argument('--cache_name', '-cn', default='C0', type=str, help='The cache name. example: C0', metavar='cache_name', dest='cache_name')
    parser.add_argument('--cache_size', '-cs', default=64, type=int, help='The cache size. example: 4096', metavar='cache_size', dest='cache_size')
    parser.add_argument('--cache_assoc', '-ca', default=4, type=int,help='The cache associativity. example: 4', metavar='cache_associativity', dest='cache_assoc')
    parser.add_argument('--cache_wr_policy', '-cwp', default='wb', type=str, choices = ['wb','wt'], help='The cache write policy. write back or write through', 
                        metavar='cache_write_policy', dest='cache_wr_policy')
    parser.add_argument('--mem_name', '-mn', default='M0', type=str, help='The external memory name. example: M0', metavar='mem_name', dest='mem_name')
    parser.add_argument('--mem_size', '-ms', default=128, type=int, help='The external memory size. example: 16384', metavar='mem_size', dest='mem_size')
    parser.add_argument('--ins_file', '-if', type=str, help='File with sequence of instructions for cache simulator.', metavar='ins_file', dest='ins_file')

    args = parser.parse_args()

    cache_sim_params = {}
    cache_sim_params['cache_name'] = args.cache_name
    cache_sim_params['cache_size'] = args.cache_size
    cache_sim_params['cache_assoc'] = args.cache_assoc
    cache_sim_params['cache_wr_policy'] = args.cache_wr_policy
    cache_sim_params['mem_name'] = args.mem_name
    cache_sim_params['mem_size'] = args.mem_size
    cache_sim = cache_simulator(cache_sim_params)

    if args.ins_file:
        cache_ops = args.ins_file
    else:
        cache_ops = 'ins/default_ins.txt'

    cache_sim.run(cache_ops)

if __name__ == '__main__':
    main()



