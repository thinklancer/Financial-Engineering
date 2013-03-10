# homework 2
from bfc import *

if __name__ == '__main__':
    q = Binomial()
    '''
    q.setFromBS(0.25,0.02,15,0.01,0.3,100,110,'american','call')
    print "Q1: option price: {0:4}".format(q.calcOptionPrice())

    q2 = q
    q2.type[1]='put'
    print "Q2: option price: {0:4}".format(q2.calcOptionPrice())

    q6 = q
    q6.setFromBS(0.25,0.02,15,0.01,0.3,100,110,'american','call')
    q6.n = 10
    print "Q6: option price: {0:4}".format(q6.calcOptionPrice())
    '''
    q8 = q
    q8.setFromBS(0.25,0.02,15,0.01,0.3,100,100,'european','call')
    q8.n = 10
    q8a = q8
    a=q8a.calcOptionPrice()
    q8b = q8
    q8b.type[1]='put'
    b=q8b.calcOptionPrice()
    print max(a,b)
