'''
.. module:: bfc

   Basic Financial Calculation
   --  Present/Future Value --
   --  Option pricing --
'''

import numpy as np
from operator import mul
from math import *
from scipy.misc import comb

def calcPV(p,n,r):
    '''
   calcPV(p,n,r)
   Args:
      p (float) : future value
      n (int) : number of periods
      r (float) : interest for each periods
   Returns:
      float.  The present value of the cash flow
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
    
#   option pricing    #
class Binomial:
    def __init__(self): # create default model
        self.setup(100,3,1.07,0.01,100.,'european','call',0)

    def display(self):
        ''' display basic information
        '''
        print "####################################"
        print "u/d: {0:4}/{1:4}".format(self.u,self.d)
        print "price/strike: {0:5}/{1:5}".format(self.price,self.strike)
        print "period: {0:d}".format(self.n)
        print "interest: {0:5}%".format((self.R-1)*100)
        print "coupon/dividend ratio {0:4}%".format(self.c*100)
        print self.type
        print "q: {0:6}".format(self.q)
        print "####################################"
        
    def setup(self,p,n,u,r,s,ae,cp,c):
        self.u=u
        self.d=1./u
        self.price=p
        self.n=n
        self.R=1+r
        self.strike=s
        self.c = c # coupon rate / dividend
        self.type=[ae,cp]
        self.checkArbitrage()
        self.setRNP()
        
        
    def calcOptionPrice(self):
        self.display()
        if self.type[1] == 'call':
            return self.calcCall()
        if self.type[1] == 'put' and self.type[0]=='american':
            return self.calcAmericanPut()
        if self.type[1] == 'put' and self.type[0]=='european':
            return self.calcEuropeanPut()

    def checkArbitrage(self):
        if self.u < 1.:
            print "!! no price up is wrong!!",self.u
        if self.u < self.R:
            print "!! arbitrage by short sell stock !!",self.u,self.R
        if self.d > self.R:
            print "!! arbitrage by borrow cash to buy !!",self.d,self.R

    def setRNP(self):
        ''' return risk neutra probabilities
        '''
        self.checkArbitrage()
        self.q = (self.R-self.d-self.c)/(self.u-self.d)
    
    def setStockPrice(self,t):
        ''' return stock price at time t
        '''
        return np.array([(self.u)**i*(self.d)**(t-i)\
                         for i in range(t,-1,-1)])*self.price
    
    def calcCall(self):
        ''' calculate call option price
            the prices for american and european are same
        '''
        Cf = self.setStockPrice(self.n)-self.strike
        Cf = np.maximum(Cf,np.zeros_like(Cf))
        qv = [(self.q)**i*(1-self.q)**(self.n-i)*comb(self.n,i)\
              for i in range(self.n,-1,-1)]
        return np.dot(Cf,qv)/self.R**self.n
        
    def calcEuropeanPut(self):
        Cf = self.strike-self.setStockPrice(self.n)
        Cf = np.maximum(Cf,np.zeros_like(Cf))
        qv = [(self.q)**i*(1-self.q)**(self.n-i)*comb(self.n,i)\
              for i in range(self.n,-1,-1)]
        return np.dot(Cf,qv)/self.R**self.n

    def calcAmericanPut(self):
        ''' return the American put option price
        '''
        for i in range(self.n,0,-1):
            #print "time step {0}/{1}".format(i,self.n)
            if i==self.n:
                Cf = self.strike-self.setStockPrice(i)
                Cf = np.maximum(Cf,np.zeros_like(Cf))
            else:
                Cf = self.strike-self.setStockPrice(i)
                Cft = np.maximum(Cf,np.zeros_like(Cf))
                Cf = np.maximum(Cft,pCf)
                '''
                if not (Cf == Cft).all():
                    print "Optimal exercise early at {0}".format(i)
                    print Cft
                    print Cf
                '''
            pCf = [onePeriodPrice(Cf[j],Cf[j+1],self.q,(self.R-1)) \
                       for j in range(0,i)]
        return max(self.strike-self.price,pCf[0])

    def calcForwards(self):
        ''' return the forwards price
        '''
        Cf = self.setStockPrice(self.n)-self.strike
        qv = [(self.q)**i*(1-self.q)**(self.n-i)*calcPerm(self.n,i)\
              for i in range(self.n,-1,-1)]
        return np.dot(Cf,qv)/self.R**self.n

    def setFromBS(self,T,r,n,c,sigma,p,s,ae,cp):
        ''' set parameters by Black Scholes Model
        '''
        self.R = exp(r*T/n)
        self.c = self.R-exp((r-c)*T/n)
        self.u = exp(sigma*sqrt(T/n))
        self.d=1./self.u
        self.price = p
        self.n = n
        self.strike = s
        self.type=[ae,cp]
        self.checkArbitrage()
        self.setRNP()
        
class BlackScholes:
    def __int__(self):
        self.S0 = 100
        self.mu = 0 # irrelevent
        self.sigma = 0.3
        self.c = 0.
        
