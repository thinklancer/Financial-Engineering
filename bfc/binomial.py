'''
Option pricing
---------------------

'''

class Binomial:
    '''
    Binomial model for option pricing

    '''
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
        ''' set up the basic information for binomial model

        :param p: current price
        :param n: number of period
        :param u: price for up / current price
        :param r: cash interest rate
        :param s: strike price
        :param ae: option type "american" / "european"
        :param cp: option type "call" / "put"
        :param c: coupon rate
        '''
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
        ''' driver to calculate the option price
        '''
        self.display()
        if self.type[1] == 'call' and self.type[0]=='european':
            return self.calcCall()
        if self.type[1] == 'call' and self.type[0]=='american':
            return self.calcCall()
        if self.type[1] == 'put' and self.type[0]=='american':
            return self.calcAmericanPut()
        if self.type[1] == 'put' and self.type[0]=='european':
            return self.calcEuropeanPut()

    def checkArbitrage(self):
        ''' check up price and interest rate prevent arbitrage oppotunity
        '''
        if self.u < 1.:
            print "!! no price up is wrong!!",self.u
        if self.u < self.R:
            print "!! arbitrage by short sell stock !!",self.u,self.R
        if self.d > self.R:
            print "!! arbitrage by borrow cash to buy !!",self.d,self.R

    def setRNP(self):
        ''' return risk neutral probabilities
        '''
        self.checkArbitrage()
        self.q = (self.R-self.d-self.c)/(self.u-self.d)
    
    def setStockPrice(self,t):
        ''' return stock price at time t
        :param t: time step t
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
            print "time step {0}/{1}".format(i,self.n)
            if i==self.n:
                Cf = self.strike-self.setStockPrice(i)
                Cf = np.maximum(Cf,np.zeros_like(Cf))
            else:
                Cf = self.strike-self.setStockPrice(i)
                Cft = np.maximum(Cf,np.zeros_like(Cf))
                Cf = np.maximum(Cft,pCf)
                if not (pCf == Cf).all():
                    print Cft
                    print np.array(pCf)
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
'''    os.system("dot -Tps "+filename+".dot -o temp.ps")
    os.system("ps2pdf temp.ps")
    os.system("mv temp.pdf "+filename+".pdf")
'''


'''
===========================
'''

import bfc.BinomialTree as BT

def setShortRateLattice(r0,u,d,n):
    ''' set short rate lattice

    :param r0: interest rate at time 0
    :param u: up move of interest rate
    :param d: down move of interest rate
    :param n: total period n
    
    '''
    bt = BT.BinomialTree(n+1)
    for i in range(n+1):
        for j in range(i+1):
            bt.setNode(i,j,r0*u**(i-j)*d**j)
    return bt

def setZCB(srl,p=100,qu=0.5,n=-1):
    ''' calculate the price structure of Zero-Coupon-Bond

    :param srl: short rate lattice
    :param p: strike price
    :param qu: up move probability
    :param n: expiration time
    :returns: the zero coupon bond lattice
    '''
    if n == -1:
        n = srl.n
    elif n >= srl.n:
        print "! wrong expiration time n!"
        exit()
    else:
        n=n+1
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(n-1,i,p)
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    return bt

def setCouponBond(srl,p=100,c=0.1,qu=0.5,n=-1):
    ''' calculate the price structure of Coupon-Bearing Bond

    :param srl: short rate lattice
    :param p: strike price
    :param c: coupon rate
    :param qu: up move probability
    :param n: expiration time
    :returns: the coupon-bearing bond lattice
    '''
    if n == -1:
        n = srl.n
    elif n > srl.n:
        print "! wrong expiration time n!"
        exit()
    else:
        n=n+1
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(n-1,i,p+p*c)
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j))+p*c)
    bt.setNode(0,0,bt.getNode(0,0)-p*c) # correct last step - no coupon at time 0
    return bt
    
def calcR(srl,n,qu=0.5):
    ''' calculate the cash account price for 1 dollar at time n

    :param srl: short rate lattice
    :param n: time n
    :returns: E[1/Bn]
    '''
    n=n+1
    if n > srl.n:
        print "! wrong expiration time n!"
        exit()
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(n-1,i,1.)
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    return bt.getNode(0,0)

def callBond(strike,expire,bond,srl,qu=0.5,outputfile=''):
    ''' calculate the Call option on the Binomial Bond

    :param strike: strike price
    :param expire: time for expiration
    :param zcb: underline zero coupon bond
    :param srl: underline short rate lattice
    '''
    n = expire+1
    if n > srl.n or n > bond.n:
        print "! wrong expiration time n!"
        exit()
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(expire,i,max(0,bond.getNode(expire,i)-strike))
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    if outputfile:
        with open(outputfile,'w') as f:
            bt.showData(f,form='{0:.2f}')
    return bt.getNode(0,0)

def forwardBond(bond,expire,srl,qu=0.5,c=0.):
    ''' calculate the price of forward on Bond

    :param bond: underline bond
    :param expire: forward mature time
    :param srl: short rate lattice
    :param qu: up move probability
    :param c: coupon rate
    '''
    n = expire+1
    if n > srl.n or n > bond.n:
        print "! wrong expiration time n!"
        exit()
    coupon = bond.getNode(bond.n-1,1) / (1+c) *c # calculate the coupon
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(expire,i,bond.getNode(expire,i)-coupon) # remove the coupon at expiration date
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    return bt.getNode(0,0)/calcR(srl,expire)


def futureBond(bond,expire,srl,qu=0.5,c=0.):
    ''' calculate the price of forward on Bond

    :param bond: underline bond
    :param expire: forward mature time
    :param srl: short rate lattice
    :param qu: up move probability
    :param c: coupon rate
    '''
    n = expire+1
    if n > srl.n or n > bond.n:
        print "! wrong expiration time n!"
        exit()
    coupon = bond.getNode(bond.n-1,1) / (1+c) *c # calculate the coupon
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(expire,i,bond.getNode(expire,i)-coupon) # remove the coupon at expiration date
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j)))
    return bt.getNode(0,0)

def bondlet(expire,srl,strike,qu=0.5,type='cap'):
    ''' calculate the price of caplet/floorlet

    :param expire: expire time (arrear settle)
    :param srl: short rate lattice
    :param strike: strike rate
    :param qu: up move probability
    :param type: cap/floor
    :returns: caplet price
    '''
    if type == 'cap':
        coef=1
    else: # 'floor'
        coef=-1
    if expire > srl.n:
        print "! wrong expiration time n!"
        exit()
    n = expire
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(n-1,i,max(coef*(srl.getNode(n-1,i)-strike),0)/(1+srl.getNode(n-1,i)))
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    return bt.getNode(0,0)
    
def swap(expire,srl,fr,qu=0.5,pay='fix',start=0):
    ''' calculate the price of Swaps

    :param expire: expire time (arrear settle)
    :param srl: short rate lattice
    :param fr: fix rate
    :param qu: up move probability
    :returns: swaps lattice
    '''
    if expire >= srl.n:
        print "! wrong expiration time n!"
        exit()
    if pay == 'fix':
        coef = 1
    else:
        coef = -1 # pay float receive fix
    n = expire+1
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # set initial payment
    for i in range(n):
        bt.setNode(n-1,i,(coef*(srl.getNode(n-1,i)-fr)/(1+srl.getNode(n-1,i))))
    # construct backwards
    for i in range(n-2,start-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,((coef*(srl.getNode(i,j)-fr)+qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j))))
    for i in range(start-1,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,((qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j))))
    return bt

def swaption(swap,srl,strike,expire,qu=0.5):
    ''' calculate the price of Swaption

    :param swap: underline swap
    :param srl: short rate lattice
    :param strike: strike rate
    :param expire: expire time
    :param qu: up move probability
    :returns: swapion price at time 0
    '''    
    n = expire+1
    if n>swap.n or n>srl.n:
        print "! wrong expiration time n!"
        exit()
    qd = 1-qu
    bt = BT.BinomialTree(n)
    # last time step
    for i in range(n):
        bt.setNode(n-1,i,max(swap.getNode(n-1,i)-strike,0))
    for i in range(n-2,-1,-1):
        for j in range(i+1):
            bt.setNode(i,j,(qu*bt.getNode(i+1,j+1)+qd*bt.getNode(i+1,j))/(1+srl.getNode(i,j)))
    return bt.getNode(0,0)


def elementarySecurity(srl,qu=0.5):
    ''' build elementary security lattice

    :param srl: short rate lattice
    :returns: state price lattice
    '''
    n = srl.n
    bt = BT.BinomialTree(n)
    qd = 1-qu
    bt.setNode(0,0,1)
    for i in range(1,n):
        # j=0 case
        bt.setNode(i,0,bt.getNode(i-1,0)/2./(1+srl.getNode(i-1,0)))
        for j in range(1,i):
            bt.setNode(i,j,0.5*(bt.getNode(i-1,j-1)/(1+srl.getNode(i-1,j-1))+bt.getNode(i-1,j)/(1+srl.getNode(i-1,j))))
        # j=i case
        bt.setNode(i,i,0.5*(bt.getNode(i-1,i-1)/(1+srl.getNode(i-1,i-1))))
    return bt




if __name__=="__main__":
    import os
    a = setShortRateLattice(0.06,1.25,0.9,6)
    
    #b = setCouponBond(a,c=0.1)
    #print forwardBond(b,4,a,c=0.1)
    #print futureBond(b,4,a,c=0.1)
    #print bondlet(6,a,0.02,type='floor')
    c = swap(5,a,0.05)
    print c.getNode(0,0)
    #print swaption(c,a,0.,3)
    #callZCB(84,2,b,a,outputfile='test.dot')
    d=elementarySecurity(a)
    price = 0
    for i in range(2,4):
        s = [(0.07-a.getNode(i-1,j))/(1+a.getNode(i-1,j))*d.getNode(i-1,j) for j in range(i)]
        price += sum(s)
    print price*1000000
    #with open('test.dot','w') as f:
    #a.showData(f,form='{0:.2f}%',coef=100)
        #b.showData(f,form='{0:.2f}')
    '''
    os.system("dot -Tps test.dot -o test.ps")
    os.system("ps2pdf test.ps")
    os.system("mv test.pdf test.pdf")
    '''
