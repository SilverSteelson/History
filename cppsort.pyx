# distutils: language=c++
from libcpp.algorithm cimport sort

def cppsort(int[:] x):
    sort(&amp;x[0], &amp;x[-1] + 1)