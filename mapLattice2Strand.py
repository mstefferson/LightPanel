#!/usr/bin/python

def mapLattice2Strand( m, n ):
    M = 5;
    N = 6;
    ind = 0;
    if m % 2 == 0:
        print("m is even")
        ind = m * N + n
    else:
        print("m is odd")
        ind = (m+1)*N - (n+1)
    return ind;
    
