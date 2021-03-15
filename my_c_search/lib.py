from ctypes import *

##wrapp of C-API DLL searcher function
lib = cdll.search 
search = lib.search_binary
#c_int_p = POINTER(c_uint32)
c_int_p = POINTER(c_int)
search.resttype = c_bool
search.argtypes = [c_int_p,c_int,c_int,c_int]
