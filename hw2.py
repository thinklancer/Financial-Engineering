# homework 2
from bfc import *

def calcAmericanCall(sel):
        for i in range(sel.n,0,-1):
            print "time step {0}/{1}".format(i,sel.n)
            if i==sel.n:
                Cf = sel.setStockPrice(i)-sel.strike
                Cf = np.maximum(Cf,np.zeros_like(Cf))
            else:
                Cf = sel.setStockPrice(i)-sel.strike
                Cft = np.maximum(Cf,np.zeros_like(Cf))
                Cf = np.maximum(Cft,pCf)
                if (Cf-pCf<0.01).any():
                    print Cft
                    print np.array(pCf)
            pCf = [onePeriodPrice(Cf[j],Cf[j+1],sel.q,(sel.R-1)) \
                       for j in range(0,i)]
        return max(sel.strike-sel.price,pCf[0])

if __name__ == '__main__':
    q = Binomial()
    
    q.setFromBS(0.25,0.02,15,0.01,0.3,100,110,'american','call')
    #print "Q1: option price: {0:4}".format(q.calcOptionPrice())

    q2 = q
    q2.type[1]='put'
    print "Q2: option price: {0:4}".format(q2.calcOptionPrice())
    
    q6 = q
    q6.setFromBS(0.25,0.02,15,0.01,0.3,100,110,'american','call')
    q6.n = 10
    print "Q6: option price: {0:4}".format(calcAmericanCall(q6))
    
    q8a = Binomial()
    q8a.setFromBS(0.25,0.02,15,0.01,0.3,100,100,'european','call')
    q8b = Binomial()
    q8b.setFromBS(0.25,0.02,15,0.01,0.3,100,100,'european','put')

    Cfcall = q8a.setStockPrice(15)-q8a.strike
    Cfcall = np.maximum(Cfcall,np.zeros_like(Cfcall))
    Cfput = q8b.strike - q8b.setStockPrice(15)
    Cfput = np.maximum(Cfput,np.zeros_like(Cfput))
    for i in range(15,0,-1):
        print "time step {0}/15".format(i)
        if i > 10:
            Cfcall = [onePeriodPrice(Cfcall[j],Cfcall[j+1],q8a.q,(q8a.R-1)) \
                       for j in range(0,i)]
            Cfput =  [onePeriodPrice(Cfput[j],Cfput[j+1],q8b.q,(q8b.R-1)) \
                       for j in range(0,i)]
        if i == 10:
            Cf = np.maximum(Cfcall,Cfput)
            print Cf
        if i <= 10:
            Cf = [onePeriodPrice(Cf[j],Cf[j+1],q8a.q,(q8a.R-1)) \
                       for j in range(0,i)]
    print Cf
    
