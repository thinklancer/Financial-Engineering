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
    ''' calculate the present value
    :param p: future value
    :param n: number of periods
    :param r: interest for each periods
    :returns: The present value of the future value
    '''
    return p*(1-(r+1)**(-n))/(1-1/(1+r))

def calcFV(p,n,r):
    ''' calcualte the future value

    :param p: present value
    :param n: number of periods
    :param r: interest for each periods
    :returns: The future value of the present value
    '''
    return p*((r+1)**n-1)/r

def calcDis(r,t):
    ''' calculate the discount rate

    :param r: interest rate
    :param t: number of periods
    :returns: discount rate
    '''
    return 1/(r+1)**t

def calcPerm(n,m):
    ''' return permunation number of m within n

    :param n: total number of choices
    :param m: number of chosens
    :returns: number of permutation
    '''
    if m==0 or m==n:
        return 1
    t = max(m,n-m)
    return reduce(mul, [i for i in range(n,t,-1)])

def onePeriodPrice(Cu,Cd,q,r):
    ''' return the one period option price for binomial model

    :param Cu: up price
    :param Cd: down price
    :param q: neutral risk probability
    :param r: cash interest
    :returns: price for previous period 
    '''
    if q <= 0 or q>=1:
        print "!! q value is wrong !!"
    return (q*Cu+(1-q)*Cd)/(1+r)

        
