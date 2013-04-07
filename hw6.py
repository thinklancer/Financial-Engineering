import bfc.BinomialTree as BT
import bfc.binomial as bino

if __name__ == "__main__":
    n = 10
    u = 1.1
    d = 0.9
    r0 = 0.05
    a = 0.01
    b = 1.01
    rec = 0.2
    F = 100

    qu = 0.5
    qd = 1-0.5
    
    # set up short rate lattice
    rlat = bino.setShortRateLattice(0.05,1.1,0.9,n)

    # set up default probability
    hlat = BT.BinomialTree(n+1)
    for i in range(n+1):
        for j in range(i+1):
            hlat.setNode(i,j,a*b**(j-i/2.))


    # set up price
    z = BT.BinomialTree(n+1)
    i = n
    for j in range(i+1):
        z.setNode(i,j,F)

    for i in range(n-1,-1,-1):
        for j in range(i+1):
            nondef = (1-hlat.getNode(i,j))*(qu*z.getNode(i+1,j+1)+qd*z.getNode(i+1,j))
            defau = hlat.getNode(i,j)*F*rec
            z.setNode(i,j,(nondef+defau)/(1+rlat.getNode(i,j)))

    print z.getNode(0,0)

    with open('hlat.dot','w') as f:
        z.showData(f,form='{0:.2f}',coef=1)
