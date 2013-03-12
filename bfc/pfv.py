'''
Present/Future Value
------------------------------------
'''

import numpy as np
from operator import mul
from math import *
from scipy.misc import comb
from IPython import embed



def calcPV(p,n,r):
    '''
    :param p: future value
    :param n: number of periods
    :param r: interest for each periods
    :returns: The present value of the cash flow
    '''
    return p*(1-(r+1)**(-n))/(1-1/(1+r))

# calcualte the future value
# input: present value, number of periods, interest for each periods
def calcFV(p,n,r):
    return p*((r+1)**n-1)/r

# calculate the discount rate
# input: interest rate and number of periods
def calcDis(r,t):
    return 1/(r+1)**t

def calcPerm(n,m):
    ''' return permunation number of m within n
    '''
    if m==0 or m==n:
        return 1
    t = max(m,n-m)
    return reduce(mul, [i for i in range(n,t,-1)])

def onePeriodPrice(Cu,Cd,q,r):
    ''' return the one period option price
    '''
    if q <= 0 or q>=1:
        print "!! q value is wrong !!"
    return (q*Cu+(1-q)*Cd)/(1+r)

        
