# solution for homework 5

import bfc.binomial as bi

if __name__ == "__main__":
    srl = bi.setShortRateLattice(0.05,1.1,0.9,10)
    zcb = bi.setZCB(srl)

    # question 1
    print zcb.getNode(0,0)

    # question 2
    print bi.forwardBond(zcb,4,srl)

    # question 3
    print bi.futureBond(zcb,4,srl)

    # question 4
    print bi.callBond(80,6,zcb,srl)
