# Author / Maintainer : Rejoy Roy Mathews

class replacement_policy(object):
    '''Base class for replacement policies.A specific cache configuration
    needs to be passed to the replacement policy to enable replacement policy
    attributes being configured
    '''

    def __init__(self, size : int = 0, associativity : int = 0) -> None:
        self._cache_size          = int(size)
        self._cache_associativity = int(associativity)
        self._cache_entries       = int(self._cache_size / 4) # integer entries in the Cache are 4 bytes
        self._cache_sets          = int(self._cache_entries / self._cache_associativity)

    def compute_to_evict(self) -> None :
        '''Runtime error if this function is invoked. This is meant to be
        a purely virtual function which must be implemented in a derived class
        '''
        raise RuntimeError('Replacement policy does not have a method to compute \
              which cache index to evict')