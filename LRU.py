import replacement_policy  as replacement_policy
class LRU(replacement_policy):
    '''This class return the index of an entry within a set that needs to be  \
    replaced'''

    def __init__(self) -> None:
        super().__init__()
        self._age_vector = []

        # Initialize age vector to all 0's
        for x in range (self._cache_entries):
            self._age_vector.append(0)

    def compute_to_evict(self, set_id : int) -> int :
        '''Compute which entry in the cache set to evict'''

        max_age = self._age_vector[set_id*self._associativity]
        replace_index = 0
        
        # Replace set entry with max age. Alternatively, a set entry that was
        # the least recently used (LRU)
        for x in range(set_id*self._associativity, set_id*self._associativity+self._associativity):
            if(self._age_vector[x] > max_age):
                max_age = self._age_vector
                replace_index = x

        for x in range(set_id*self._associativity, set_id*self._associativity+self._associativity):
            if(x == replace_index):
                self._age_vector[x] = 0
            else:
               self._age_vector[x] += 1

        return replace_index - set_id*self._associativity