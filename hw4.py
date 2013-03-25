from scipy.misc import comb
import numpy as np

def qs5():
    n = 15
    r = 12
    p = 0.5
    px = [ comb(n,i)*p**i*(1-p)**(n-i) for i in range(r,n+1)]
    print np.sum(px)

def qs6():
    n = 15
    r = 14
    p = 0.5
    px = [comb(n,i)*p**i*(1-p)**(n-i) for i in range(r,n+1)]
    px = np.sum(px)
    print px
    pv = 1-(1-px)**100
    print pv

if __name__=="__main__":
    qs5()

