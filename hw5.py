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

    # question 5
    d = bi.elementarySecurity(srl)
    price = 0
    for i in range(2,12):
        s = [(srl.getNode(i-1,j)-0.045)/(1+srl.getNode(i-1,j))*d.getNode(i-1,j) for j in range(i)]
        price += sum(s)
    print price*1000000

    # question 6
    e = bi.swap(10,srl,fr=0.045,start=1)
    print bi.swaption(e,srl,0,5)*1000000

    # another way
    f = bi.elementarySecurity(srl)
    price = 0
    for i in range(6,12):
        s = [(srl.getNode(i-1,j)-0.045)/(1+srl.getNode(i-1,j))*d.getNode(i-1,j) for j in range(i-3)]
        print s
        price += sum(s)
    print price*1000000

