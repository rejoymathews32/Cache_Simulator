# Author / Maintainer : Rejoy Roy Mathews

from replacement_policy  import replacement_policy

class LRU(replacement_policy):
    '''Return the least recenty used entry in a cache set.
    This entry can then be replaced with a new cache entry
    '''

    def __init__(self, size : int = 64, associativity : int = 1) -> None:
        super().__init__(size, associativity)
        self._age_vector = [] # LRU keeps track of age for all cache entries        
        for x in range (self._cache_entries): # Initialize age for all cache entries to 0
            self._age_vector.append(0)

    def compute_to_evict(self, set_id : int) -> int :
        '''
        This method accepts the cache set ID. The entry in the cache set which
        has been used least recently will be evicted. LRU increaments
        the age of all the entries in a set by one upon cache set access.
        The age of the cache set entry that was accessed is set to 0. The least
        recently used entry is the entry with the highest age
        '''        
        set_base_addr = set_id*self._cache_associativity
        replace_index = set_base_addr
        max_age = self._age_vector[set_base_addr]
        # Compute the max age and replacement index for a set
        for idx in range(set_base_addr,set_base_addr+self._cache_associativity):
            if(self._age_vector[idx] > max_age):
                max_age = self._age_vector[idx]
                replace_index = idx

        return replace_index - set_base_addr

    def cache_ent_acc(self, cache_idx) -> None :
        '''
        This method accepts the cache index and computes the cache set from the index.
        It recomutes the age for all the entries in the set upon every new
        access to any member in the set
        '''
        set_idx = int(cache_idx/self._cache_associativity)
        set_ent_st_idx = set_idx*self._cache_associativity
        # Run over all the entries in the cache set and update age
        for idx in range(set_ent_st_idx,set_ent_st_idx+self._cache_associativity):
            if(idx == cache_idx):
                self._age_vector[idx] = 0
            else:
               self._age_vector[idx] += 1        

    @property
    def name(self) -> str:
        '''Defines the replacement policy name'''
        return 'Least Recently Used (LRU) replacement policy'