import math as math

class replacement_policy(object):
    '''Defining the base class for replacement policies. \
        A replacement policy operates on a cache with a specific \
        cache size and cache associativity'''

    def __init__(self, size : int, associativity : int) -> None:
        if(not(math.log2(size).is_integer())):
            assert ValueError('Cache size must be a power of 2')
        
        if(not(math.log2(associativity).is_integer())):  
            assert ValueError('Associativity must be a power of 2. Associativty "1" represents \
            direct-mapped and associativity "0" represents fully-associative')

        self._cache_size = size
        self._cache_associativity = associativity
        self._cache_entries = self._cache_size / 4 # integer entries in the Cache are 4 bytes
        self._cache_sets = self._cache_entries / self._cache_associativity

    def compute_to_evict(self, set_id : int) -> int :
        # Derived classes need to override this implementation of
        # which entry in the set to evict
        return 0