# Welcome to the Cache Simulator

This projects simulates a cache with a specific size(in Bytes), associativity and write policy and computes the cache hits and cache misses for a specific cache memory access sequence of instructions. The cache can model any CPU cache level and expects a reference to the next level of cache(or main memory) to allows fetching the data from the next level incase of a cache miss. The current implementation supports the LRU (Least Recently Used) replacement policy but is confiurable to support any newly implemented replacement policy.

## Cache Simulator parameters
* *Cache size* - The cache size in Bytes must be a power of *2*. The cache size is constrained to *>=64B* and *<=64MB*
* *Cache associativity* - The cache associaitivty is a power of *2* and is constrained to *>=1* and *<=16*
* *Cache write policy* - The cache supports the write back *(wb)* and the write through *(wt)* write policies
* *Memory size* - Memory size represents the next level of memory in the hierarchy the cache is being simulated for. The memory size in Bytes must be a power of *2*. The cache size is constrained to *n\*cache_size* where *n* is constrained to *n>1* 