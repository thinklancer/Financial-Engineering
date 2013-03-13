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
