'''
Portfolios related calculation
==============================
'''

import numpy as np
from math import *

def var_risk_asset(r,mu,sig):
    ''' calculate the minimum variance portfolio

    minimize L = sum_i,sum_j(sig_ij*xi*xj) - v*[sum_i(mu_i*xi)-r) - u*[sum_i(xi)-1]
    --> 2 sum_j(sig_ij*xi)-v*mu_i-u=0
    
    :param r: required return rate
    :param mu: mean return for assets
    :type mu: numpy array
    :param sig: covariance matrix for assets
    :type sig: numpy matrix
    :returns: minimum variance portfolio
    '''
    n = len(mu)
    A = np.zeros((n+2,n+2))
    A[:n,:n]=sig*2
    A[:n,n]=0-mu
    A[n,:n]=mu
    A[n+1,:n]=1
    A[:n,n+1]=-1

    b = np.zeros(n+2)
    b[n:] = [r,1]
    
    x = np.array(np.dot(np.matrix(A).I,b))
    x.shape=-1
    return x[:n]

def var_riskfree_asset(mu,sig,rf):
    ''' calculate the max return portfolio with risk-free asset (rf)

    max rf+sum_i[(mu_i-rf)*xi]-tau*[sum_i,sum_j(sig_ij*xi*xj)]
    --> x = V^-1 mu' / 2tau
    V = sig, mu'=mu-rf

    :param mu: mean return for assets
    :type mu: numpy array
    :param sig: covariance matrix for assets
    :type sig: numpy matrix
    :param rf: risk-free return rate
    :returns: max return portfolio (with normalized to 1)
    '''
    x = np.array(np.dot(sig.I,mu-rf))
    x.shape=-1
    return x/np.sum(x)

def min_var_risk_asset(mu,sig):
    ''' calculate the minimum variance of given asset
    min sum_i,sum_j(sig_ij*xi*xj) under sum_i xi=1
    sum_j (sig_ij*xj)-u=0
    sum_j xj = 1

    :param mu: mean return for assets
    :type mu: numpy array
    :param sig: covariance matrix for assets
    :type sig: numpy matrix
    '''
    n = len(mu)
    A = np.zeros([n+1,n+1])
    A[:n,:n] = sig
    A[:n,n] = -1
    A[n,:n] = 1
    b = np.zeros(n+1)
    b[n]=1
    x = np.array(np.dot(np.matrix(A).I,b))
    x.shape=-1
    return x[:n]
    
    
class portf:
    def __init__(self):
        x = [] # array
        sig = np.matrix([])
        mu = []
        rf = 0.

    def selfcheck(self):
        nx = len(self.x)
        if nx != len(self.mu) or (nx,nx != sig.shape):
            print "!the shape of portfolio's return/variance is wrong!"

    def calcReturn(self):
        ''' calculate the return of the portfolio
        '''
        return np.sum(self.x*self.mu)

    def calcVolatility(self):
        ''' calculate the volatility of the portfolio
        '''
        return sqrt(np.dot(self.x,np.dot(self.sig,self.x).T)[0,0])
