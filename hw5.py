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
    import bfc.BinomialTree as BT
    n = srl.n
    expire = 5
    bt = BT.BinomialTree(n)
    qu = 0.5
    qd = 1-qu
    fr = 0.045
    bt.setNode(0,0,1)
    for i in range(1,n):
        # j=0 case
        bt.setNode(i,0,bt.getNode(i-1,0)/2./(1+srl.getNode(i-1,0)))
        for j in range(1,i):
            bt.setNode(i,j,0.5*(bt.getNode(i-1,j-1)/(1+srl.getNode(i-1,j-1))+bt.getNode(i-1,j)/(1+srl.getNode(i-1,j))))
        # j=i case
        bt.setNode(i,i,0.5*(bt.getNode(i-1,i-1)/(1+srl.getNode(i-1,i-1))))
        # check option excised
        if i == expire:
            for j in range(i+1):
                if srl.getNode(i,j) < fr:
                    bt.setNode(i,j,0.)
    
    #pay = BT.BinomialTree(11)
    price = 0
    for i in range(expire,11):
        s = [(srl.getNode(i,j)-fr)/(1+srl.getNode(i,j))*bt.getNode(i,j) for j in range(i+1)]
        #for j in range(i+1):
        #pay.setNode(i,j,(srl.getNode(i,j)-0.045)/(1+srl.getNode(i,j)))  #payment lattice
        price += sum(s)
    print price*1000000
    #with open('test.dot','w') as fi:
    #pay.showData(fi,form='{0:.2f}',coef=100)
    

