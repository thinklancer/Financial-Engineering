'''
Black Scholes Model
-------------------
'''
from math import erf,sqrt,log,exp,pi
version = '1.0'

def calcN(x):
    ''' return P(N(0,1)<x)
    '''
    return (1.0 + erf(x/sqrt(2.0))) / 2.0

def calcphi(x):
    return exp(-x**2/2.)/sqrt(2*pi)

class BlackScholes:
    ''' Black Scholes Model

    '''
    def __init__(self,s0=100.,r=0.01,sigma=0.4,t=1.,dividend=0.00,k=100.):
        self.s0 = s0 # current price
        self.r = r # interest rate
        self.sigma = sigma # variance
        self.c = dividend # dividend payment
        self.t=t # time
        self.k=k  # strike price
        
        self.d1 = (log(self.s0/self.k)+(self.r-self.c+self.sigma**2/2.)*self.t)/(self.sigma*sqrt(self.t))
        self.d2 = self.d1 - self.sigma*sqrt(self.t)

    def CallPrice(self):
        ''' return the call price
        '''
        return self.s0*exp(-self.c*self.t)*calcN(self.d1) - self.k*exp(-self.r*self.t)*calcN(self.d2)

    def PutPrice(self):
        ''' return the put price
        '''
        return self.CallPrice()+self.k*exp(-self.r*self.t)-self.s0*exp(-self.c*self.t)

    def deltaC(self):
        ''' delta for call option
        '''
        return exp(-self.c*self.t)*calcN(self.d1)

    def deltaP(self):
        ''' delta for put option
        '''
        return self.deltaC()-exp(-self.c*self.t)

    def gamma(self):
        ''' gamma
        '''
        return exp(-self.c*self.t)*calcphi(self.d1)/(self.sigma*self.s0*sqrt(self.t))

    def vega(self):
        ''' vega
        '''
        return exp(-self.c*self.t)*self.s0*sqrt(self.t)*calcphi(self.d1)

    def theta(self):
        ''' theta
        '''
        return exp(-self.c*self.t)*self.s0*(-calcphi(self.d1)*self.sigma/(2*sqrt(self.t))+self.c*calcN(self.d1)) \
            - self.r*self.k*exp(-self.r*self.t)*calcN(self.d2)
        

if __name__ == "__main__":
    import numpy as np
    import matplotlib.pylab as plt

    plt.figure()
    
    def fig1():
        ''' compare Delta for European Call and Put options
        '''
        s0a = np.arange(50,150,0.1)
        y = np.empty_like(s0a,dtype=np.float)
        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5,sigma=0.3)
            y[i] = bsm.deltaC()
        plt.plot(s0a,y,label='Call Delta')

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5,sigma=0.3)
            y[i] = bsm.deltaP()
        plt.plot(s0a,y,label='Put Delta')
        plt.ylabel('Delta')
        plt.xlim(50,150)
        plt.xlabel('Stock Price at t=0')
        
    def fig2():
        ''' compare delta for different mature time t
        '''
        s0a = np.arange(50,150,0.1)
        y = np.empty_like(s0a,dtype=np.float)
        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5)
            y[i] = bsm.deltaC()
        plt.plot(s0a,y,label='T = .5 years')        

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.25)
            y[i] = bsm.deltaC()
        plt.plot(s0a,y,label='T = .25 years')

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.05)
            y[i] = bsm.deltaC()
        plt.plot(s0a,y,label='T = .05 years') 
        plt.ylabel('Delta')
        plt.xlim(50,150)
        plt.xlabel('Stock Price at t=0')

    def fig3():
        ''' compare delta for different maturity
        '''
        ta = np.arange(0.05,1,0.01)
        y = np.empty_like(ta,dtype=np.float)
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,sigma=0.5,dividend=0.03,r=0.05)
            y[i] = bsm.deltaC()
        plt.plot(ta,y,label='ATM option')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=110,sigma=0.5)
            y[i] = bsm.deltaC()
        plt.plot(ta,y,label='10% ITM')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=90,sigma=0.5)
            y[i] = bsm.deltaC()
        plt.plot(ta,y,label='10% OTM')
        plt.xlim(0,1)
        plt.ylabel('Delta')
        plt.xlabel('Time-To-Maturity')
        plt.legend()

    def fig4():
        ''' compare Gamma for European Option
        '''
        s0a = np.arange(50,150,0.1)
        y = np.empty_like(s0a,dtype=np.float)
        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5)
            y[i] = bsm.gamma()
        plt.plot(s0a,y,label='T = .5 years')        

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.25)
            y[i] = bsm.gamma()
        plt.plot(s0a,y,label='T = .25 years')

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.05)
            y[i] = bsm.gamma()
        plt.plot(s0a,y,label='T = .05 years') 
        plt.ylabel('Gamma')
        plt.xlim(50,150)
        plt.xlabel('Stock Price at t=0')

    def fig5():
        ''' compare Gamma with time-to-maturity
        '''
        ta = np.arange(0.05,1,0.01)
        y = np.empty_like(ta,dtype=np.float)
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t)
            y[i] = bsm.gamma()
        plt.plot(ta,y,label='ATM option')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=80)
            y[i] = bsm.gamma()
        plt.plot(ta,y,label='20% OTM')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=90)
            y[i] = bsm.gamma()
        plt.plot(ta,y,label='10% OTM')
        plt.xlim(0,1)
        plt.ylabel('Gamma')
        plt.xlabel('Time-To-Maturity')
        plt.legend()

    def fig6():
        ''' compare vega with stock price
        '''
        s0a = np.arange(50,150,0.1)
        y = np.empty_like(s0a,dtype=np.float)
        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5)
            y[i] = bsm.vega()
        plt.plot(s0a,y,label='T = .5 years')        

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.25)
            y[i] = bsm.vega()
        plt.plot(s0a,y,label='T = .25 years')

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.05)
            y[i] = bsm.vega()
        plt.plot(s0a,y,label='T = .05 years') 
        plt.ylabel('Vega')
        plt.xlim(50,150)
        plt.xlabel('Stock Price at t=0')

    def fig7():
        ''' compare vega with time-to-maturity
        '''
        ta = np.arange(0.05,1,0.01)
        y = np.empty_like(ta,dtype=np.float)
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t)
            y[i] = bsm.vega()
        plt.plot(ta,y,label='ATM option')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=80)
            y[i] = bsm.vega()
        plt.plot(ta,y,label='20% OTM')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=90)
            y[i] = bsm.vega()
        plt.plot(ta,y,label='10% OTM')
        plt.xlim(0,1)
        plt.ylabel('Vega')
        plt.xlabel('Time-To-Maturity')
        plt.legend()
        
    def fig8():
        ''' compare theta with stock price
        '''
        s0a = np.arange(50,150,0.1)
        y = np.empty_like(s0a,dtype=np.float)
        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.5,r=0.)
            y[i] = bsm.theta()
        plt.plot(s0a,y,label='T = .5 years')        

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.25,r=0.)
            y[i] = bsm.theta()
        plt.plot(s0a,y,label='T = .25 years')

        for i,s0 in enumerate(s0a):
            bsm = BlackScholes(s0=s0,t=0.05,r=0.)
            y[i] = bsm.theta()
        plt.plot(s0a,y,label='T = .05 years') 
        plt.ylabel('Theta')
        plt.xlim(50,150)
        plt.xlabel('Stock Price at t=0')

    def fig9():
        ''' compare Theta with time-to-maturity
        '''
        ta = np.arange(0.05,1,0.01)
        y = np.empty_like(ta,dtype=np.float)
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,r=0.)
            y[i] = bsm.theta()
        plt.plot(ta,y,label='ATM option')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=80,r=0.)
            y[i] = bsm.theta()
        plt.plot(ta,y,label='20% OTM')
        for i,t in enumerate(ta):
            bsm = BlackScholes(t=t,k=90,r=0.)
            y[i] = bsm.theta()
        plt.plot(ta,y,label='10% OTM')
        plt.xlim(0,1)
        plt.ylabel('Theta')
        plt.xlabel('Time-To-Maturity')
        plt.legend()

    fig8()
    plt.figure()
    fig9()
    plt.legend()
    plt.show()
    
