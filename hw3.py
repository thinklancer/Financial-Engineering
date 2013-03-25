'''
homework 3
==========
'''

import numpy as np
from bfc.portf import *

np.set_printoptions(precision=4)

mu = np.array([6,2,4])/100.
V = np.matrix("8 -2 4; -2 2 -2; 4 -2 8")*1e-3
rf = 0.01
    
if __name__=="__main__":
    por = portf()
    por.mu = mu
    por.sig = V
    por.rf = rf

    # qs1
    por.x = np.array([1,1,1])/3.
    print por.calcReturn()*100

    # qs2
    print por.calcVolatility()*100

    # qs3
    por.x = min_var_risk_asset(por.mu,por.sig)
    print por.calcReturn()*100

    # qs4
    por.x = var_riskfree_asset(por.mu,por.sig,por.rf)
    mus =por.calcReturn()*100
    print mus
    
    # qs5
    sigs = por.calcVolatility()*100
    print sigs
    
    # qs6
    cml = (mus-por.rf*100)/sigs
    print cml
    
    # qs7
    req = cml*5+por.rf*100
    print req
