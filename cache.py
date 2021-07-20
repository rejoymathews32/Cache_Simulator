# Author / Maintainer : Rejoy Roy Mathews

from Memory import Memory
import replacement_policy as replacement_policy
import math as math

class Cache(object):
    '''Modelling a cache which is defined by its
    Reference to the main memory,
    Reference to a cache replacement policy,
    size in Bytes - 64 Bytes to 64 Bytes range,
    associativity - 1 to 16-way associativity support,
    write policy - write back ("wb") or write through("wt") write policy support
    '''
    def __init__(self,                
                name : str = 'default',
                size : int = 64,
                associativity : int = 1,
                write_policy : str = 'wt',
                extern_memory : Memory = None,
                r_policy : replacement_policy = None
                ) -> None:
                
        # Check cache size range - 64B to 64MB
        # Check associaitivity range - 1 to 16
        # Check if cache size is a power of 2
        # Check if associativity is a power of 2
        if(not(size >= 64 and size <= 67108864) or 
            not(associativity > 0 and associativity <= 16) or
            not(math.log2(size).is_integer()) or
            not(math.log2(associativity).is_integer())):

            raise ValueError('Cache size must be a power of 2 and must be within the range \
                of 64Bytes and 64MBytes. \n \
                Associativity must be a power of 2 and must be within the range of 1 to 16. \
                Associativty "1" represents a direct-mapped cache')

        if(not(write_policy == 'wb' or write_policy == 'wt')):
            raise ValueError('Valid cache policies include write back ("wb") and write through ("wt"). \
                    Provide "wb" or "wt" as input')

        self._name                = name # Cache name
        self._write_policy        = write_policy # Cache write policy
        self._cache_size          = int(size) # Cache size
        self._cache_associativity = int(associativity) # Cache associaitivty
        self._cache_entries       = int(self._cache_size / 4) # integer entries in the Cache are 4 bytes each
        self._cache_sets          = int(self._cache_entries / self._cache_associativity) # Number of sets in a cache
        self._cache_set_bits      = int(math.log2(self._cache_sets)) # Cache set bits
        # cache tagbits = address size - size of set bits
        self._cache_tag_bits      = 32 - self._cache_set_bits
        # Instantiate cache memory
        self._cache_memory        = Memory(name+'_mem', self._cache_entries)
        # Link to the external memory and replacement policy for this cache
        self._extern_main_memory  = extern_memory
        self._replacement_policy  = r_policy
        # Define datastructure for cache entry status
        self._cache_entry_valid   = []
        # Define datastructure for cache entry tag
        self._cache_entry_tag     = []
        # Define data structure for cache entry ditry
        self._cache_entry_dirty   = []
        # Total cache memory read count
        self._cache_rd_ct  = 0
        # Total cache memory write count
        self._cache_wr_ct  = 0
        # Total cache hits
        self._cache_hits  = 0
        # Total cache misses
        self._cache_misses  = 0
        # Initialize all cache entries status and dirty bits to 0
        for x in range(self._cache_entries):
            self._cache_entry_valid.append(0)
            self._cache_entry_tag.append(0)        
            self._cache_entry_dirty.append(0)

    def _compute_cache_write_entry(self, address : int) -> int :
        '''Compute the cache entry to write to.
        If a cache set is empty the first entry in the set is selected.
        If the cache set is full the replacement policy computed entry is over-written
        If the cache is partly full, the entry with a matching tag is selected, in the
        absence of which the first unused entry is selected
        '''
        # Cache set to write to.
        cache_set_selected = int('{:032b}'.format(int(address))[self._cache_tag_bits: \
                                self._cache_tag_bits+self._cache_set_bits],2)            
        
        cache_set_empty    = 1
        cache_set_full     = 1

        set_idx = cache_set_selected*self._cache_associativity

        for entr_idx in range(set_idx,set_idx+self._cache_associativity):
            if(self._cache_entry_valid[entr_idx] == 1):
                cache_set_empty = 0
            if(self._cache_entry_valid[entr_idx] == 0):
                cache_set_full  = 0
        
        cache_idx  = 0 #Select the cache index to write to
        ent_in_cache = 0 #Check if entry exists in cache
        write_to_mem = 1 #Write to main memory

        if(cache_set_empty): # Cache is empty            
            cache_idx = set_idx # Select first entry in the set                   
        elif(cache_set_full): #Cache is full
            # Check if there is a matching tag in cache
            for entr_idx in range(set_idx,set_idx+self._cache_associativity):             
                if((self._cache_entry_valid[entr_idx] == 1) and \
                    (self._cache_entry_tag[entr_idx]  == int('{:032b}'.format(int(address))[0:self._cache_tag_bits],2))):
                    cache_idx = entr_idx
                    ent_in_cache = 1
                    write_to_mem = 0
                    break                  
            # Else compute which entry to evict
            if not (ent_in_cache):                 
                eviction_index = self._replacement_policy.compute_to_evict(cache_set_selected)
                cache_idx = set_idx + eviction_index
        else: #Cache has some entries            
            for entr_idx in range(set_idx,set_idx+self._cache_associativity):
                # Check if there is a matching tag                
                if((self._cache_entry_valid[entr_idx] == 1) and \
                    (self._cache_entry_tag[entr_idx]  == int('{:032b}'.format(int(address))[0:self._cache_tag_bits],2))):
                    cache_idx = entr_idx
                    write_to_mem = 0
                    break
                # Else write to first available entry
                elif(self._cache_entry_valid[entr_idx] == 0):
                    cache_idx = entr_idx
                    break
                
        return cache_idx, write_to_mem

    def _write_to_cache_wb(self, address : int, data : int, rd_dr_wr : bool = False) -> None:
        '''Write to a write-back cache includes writing only to the cache. \
            Writes to memory are limited to "dirty entries" in cache'''
        # Invoke the function that actually writes to the cache memory
        cache_idx, write_to_mem = self._compute_cache_write_entry(address)
        # Inform the replacement policy about a cache access
        self._replacement_policy.cache_ent_acc(cache_idx)
        if(self._cache_entry_dirty[cache_idx] and write_to_mem):
            # Write to main memory before writing to cache
            mem_addr = (self._cache_entry_tag[cache_idx] << (self._cache_set_bits)) + int(cache_idx/self._cache_associativity)
            self._extern_main_memory.memory_write(mem_addr, self._cache_memory.memory_read(cache_idx))
        
        self._cache_memory.memory_write(cache_idx, data) # Write to cache memory
        self._cache_entry_valid[cache_idx] = 1 #Mark this entry as a valid cache entry

        if(rd_dr_wr):
            self._cache_entry_dirty[cache_idx] = 0 #Dont update dirty bit for entry
        else:
            self._cache_entry_dirty[cache_idx] = 1 #Upadte dirty bit for the entry
        self._cache_entry_tag[cache_idx]   = int('{:032b}'.format(int(address))[0:self._cache_tag_bits],2)

    def _write_to_cache_wt(self, address : int, data : int) -> None:
        '''Write to a write-through cache includes writing to the cache \
            and to the memory'''        
        self._extern_main_memory.memory_write(address,data) # Always write to main memory    
        cache_idx = self._compute_cache_write_entry(address) # Compute cache write index        
        self._replacement_policy.cache_ent_acc(cache_idx) # Inform the replacement policy about a cache access
        self._cache_memory.memory_write(cache_idx, data) # writes to the cache memory
        # Write through does not have the concept of dirty bit        
        self._cache_entry_valid[cache_idx] = 1 #Mark this entry as a valid cache entry
        self._cache_entry_tag[cache_idx]   = int('{:032b}'.format(int(address))[0:self._cache_tag_bits],2) #Update set entry tag

    def write_to_cache(self, address : int, data : int, rd_dr_wr : bool = False) -> None:
        '''Write to the cache : Cache[fn(addr)] = data'''
        self._cache_wr_ct+=1
        if(self._write_policy == 'wb'):
            self._write_to_cache_wb(address,data, rd_dr_wr)
        else:
            self._write_to_cache_wt(address, data)

    def read_from_cache(self, address : int) -> hex:         
        '''Read from the cache'''
        self._cache_rd_ct+=1
        cache_set_selected = int('{:032b}'.format(int(address))[self._cache_tag_bits: \
                                 self._cache_tag_bits+self._cache_set_bits],2)

        set_idx = cache_set_selected*self._cache_associativity
        for entr_idx in range(set_idx, set_idx + self._cache_associativity):
                        if((self._cache_entry_tag[entr_idx] == int('{:032b}'.format(int(address))[0:self._cache_tag_bits],2)) and \
                         (self._cache_entry_valid[entr_idx] == 1)):
                            self._cache_hits+=1
                            # Inform the replacement policy about a cache access
                            self._replacement_policy.cache_ent_acc(entr_idx)
                            return self._cache_memory.memory_read(entr_idx)        
        # Entry not available in the cache. Read from the main memory        
        extern_memory_read = self._extern_main_memory.memory_read(address)
        # Update this read data into the cache for future use        
        self.write_to_cache(address, extern_memory_read, True)
        self._cache_misses+=1
        return extern_memory_read

    @property
    def name(self) -> str:
        '''Returns the cache name'''
        return self._name
    
    def __str__(self) -> str:
        out_str = ''
        out_str = out_str + '=======================================================\n'
        out_str = out_str + f'Cache name : {self._name} \n'           
        out_str = out_str + f'Cache size : {self._cache_size}.\n'
        out_str = out_str + f'Cache write policy : {self._write_policy}.\n'
        out_str = out_str + f'Cache replacement policy : {self._replacement_policy.name}\n'
        out_str = out_str + f'Cache Associativity : {self._cache_associativity}.\n'
        out_str = out_str + f'Cache Memory Interface : {self._extern_main_memory.name}.\n'
        out_str = out_str + '=======================================================\n'
        out_str = out_str + f'Cache dump format - Cache[set index, set entry index]\n'
        for set_idx in range(self._cache_sets):
            for set_ent_idx in range(self._cache_associativity):
                out_str = out_str + f'Cache[{set_idx},{set_ent_idx}] = \
                    {self._cache_memory.memory_read(set_idx*self._cache_associativity + set_ent_idx)}.\n'

        return out_str

    def stats(self) -> None:
        out_str = ''
        out_str = out_str + f'Cache {self._name} total reads : {self._cache_rd_ct} \n'
        out_str = out_str + f'Cache {self._name} total writes : {self._cache_wr_ct} \n'
        out_str = out_str + f'Cache {self._name} hits : {self._cache_hits} \n'
        out_str = out_str + f'Cache {self._name} misses : {self._cache_misses} \n'
        print(out_str)