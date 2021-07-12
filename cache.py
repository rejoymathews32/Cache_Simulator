import Memory as Memory
import replacement_policy as replacement_policy
import math as math

class Cache(object):
    '''This class models a cache'''
    def __init__(self, size : int, \
                associativity : int, \
                initial_value, write_policy : str, \
                extern_memory : Memory, \
                r_policy : replacement_policy) -> None:

        if(not(math.log2(size).is_integer())):
            assert ValueError('Cache size must be a power of 2')
        
        if(not(math.log2(associativity).is_integer())):  
            assert ValueError('Associativity must be a power of 2. Associativty "1" represents \
            direct-mapped')
                
        if(not(associativity > 0 and associativity <= 16) or \
            not(size >= 64 and size < 67108864)):  
            assert ValueError('Associativity supported - Direct mapped upto 16 way associative \n \
                                Cache size supported is 64Bytes upto 64 MBytes')

        try:
            if(write_policy != 'wb' or write_policy != 'wt'):
                raise ValueError
        except ValueError:
            print('Valid cache policies include write back ("wb") and write through ("wt")')
        else:
            self._write_policy = write_policy
            if(write_policy == 'wb'):
                self._cache_entry_dirty = []
                for x in range(self._cache_entries):
                    self._cache_entry_dirty.append(0)


        # To be used for cache configuration dump        
        self._cache_size = size
        self._cache_associativity = associativity
        self._cache_entries = self._cache_size / 4 # integer entries in the Cache are 4 bytes

        self._cache_set_bits = math.log2(self._cache_entries / self._cache_associativity)
        # integer bit size - size of set bits - integer log2 byte size
        self._cache_tag_bits = 32 - math.log2(self._cache_set_bits) - 2

        # Instantiate cache memory
        self._cache_memory = Memory(self._cache_entries, initial_value)

        # Link to the external memory and replacement policy for this cache
        self._extern_main_memory = extern_memory
        self._replacement_policy = r_policy

        # Define datastructure for cache entry status
        self._cache_entry_valid = []

        # Define datastructure for cache entry tag
        self._cache_entry_tag = []

        # Initialize all cache entries status and entry tags to 0
        for x in range(self._cache_entries):
            self._cache_entry_valid.append(0)
            self._cache_entry_tag.append(0)


    def _compute_cache_write_entry(self, address : int) -> int :
        '''This method implements the actual write to cache memory \
            This method will have wrpper functions around it'''

        # Cache set to write to
        cache_set_selected = int(bin(address)[2+self._cache_tag_bits:2+ \
        self._cache_tag_bits+self._cache_set_bits],2)            
        
        cache_set_empty = 1
        cache_set_full = 1

        for x in range(cache_set_selected \
                    *self._cache_associativity, \
                    cache_set_selected*self._cache_associativity \
                    + self._cache_associativity):

            if(self._cache_entry_valid[x] == 1):
                cache_set_empty = 0
                break

        for x in range(cache_set_selected \
                        *self._cache_associativity, \
                        cache_set_selected*self._cache_associativity \
                        + self._cache_associativity):

            if(self._cache_entry_valid[x] == 0):
                cache_set_full = 0
                break
        
        cache_index_selected  = 0
        # Cache is empty
        if(cache_set_empty):

            cache_index_selected = cache_set_selected*self._cache_associativity
            
        #Cache is full
        elif(cache_set_full):

            # Compute which entry to evict
            eviction_index = self._replacement_policy.compute_to_evict(cache_set_selected)
            cache_index_selected = cache_set_selected *self._cache_associativity + eviction_index

        #Cache has some entries
        else: 
            
            for x in range(cache_set_selected \
                            *self._cache_associativity, \
                            cache_set_selected*self._cache_associativity \
                            + self._cache_associativity):
                # Check if there is a matching tag                
                if((self._cache_entry_tag[x] == int(bin(address)[2:2+self._cache_tag_bits],2)) and \
                (self._cache_entry_valid[x] == 1)):
                    cache_index_selected = x
                    break

                # Else write to first available entry
                elif(self._cache_entry_valid[x] == 0):
                    cache_index_selected = x
                    break
        
        
        return cache_index_selected

    def _write_to_cache_wb(self, address : int, data : int) -> None:
        '''Write to a write-back cache includes writing only to the cache. \
            Writes to memory are limited to "dirty entries" in cache'''

        # Invoke the function that actually writes to the cache memory
        cache_index_selected = self._compute_cache_write_entry(address)

        if(self._cache_entry_dirty[cache_index_selected]):
            # Write to main memory before writing to cache
            self._extern_memory.memory_write(self._cache_memory.memory_read(cache_index_selected))

        # Write to cache memory
        self._cache_memory.memory_write(cache_index_selected, data)
        #Mark this entry as a valid cache entry
        self._cache_entry_valid[cache_index_selected] = 1
        #Upadte dirty bit for the entry
        self._cache_entry_dirty[cache_index_selected] = 1            
        #Update set entry tag
        self._cache_entry_tag[cache_index_selected] = \
        int(bin(address)[2:2+self._cache_tag_bits],2)

    def _write_to_cache_wt(self, address : int, data : int) -> None:
        '''Write to a write-through cache includes writing to the cache \
            and to the memory'''

        # Always write to main memory in a write through cache
        self._extern_main_memory.memory_write(address,data)        

        # Invoke the function that actually writes to the cache memory
        cache_index_selected = self._compute_cache_write_entry(address)

        self._cache_memory.memory_write(cache_index_selected, data)

        # Write through does not have the concept of dirty bit

        # Cache tag for cache entry
        self._cache_entry_tag = int(bin(address)[2:2+ \
        self._cache_tag_bits+self._cache_set_bits],2)

    def write_to_cache(self, address : int, data : int) -> None:
        '''Write to the cache'''
        if(self._write_policy == 'wb'):
            self._write_to_cache_wb(address,data)
        else:
            self._write_to_cache_wt(address, data)

    def read_from_cache(self, address : int) -> hex:         
        '''Read from the cache'''

        cache_set_selected = int(bin(address)[2+self._cache_tag_bits: \
                                 2+self._cache_tag_bits+self._cache_set_bits],2)

        for x in range(cache_set_selected \
                        *self._cache_associativity, \
                        cache_set_selected*self._cache_associativity \
                        + self._cache_associativity):
                        if((self._cache_entry_tag[x] == int(bin(address)[2:2+self._cache_tag_bits],2)) and \
                        (self._cache_entry_valid[x] == 1)):
                            return self._cache_memory.memory_read(x)
        
        # Entry not available in the cache
        # Read from the main memory        
        extern_memory_read = self._extern_main_memory.memory_read(address)

        # Update this read data into the cache for future use
        self.write_to_cache(address, extern_memory_read)

        return extern_memory_read





        

                

    
    
    #RRM - define this
    def __str__(self) -> str:
        return super().__str__()            





    

