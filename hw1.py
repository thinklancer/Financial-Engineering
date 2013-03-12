'''
homework 1
==========
'''
def calcPV(p,n,r):
    return p*(1-r**(-n))/(1-1/r)

def calcFV(p,n,r):
    return p*(r**n-1)/(r-1)

def calcDis(r,t):
    return 1/r**t

'''
Lottery payments

A major lottery advertises that it pays the winner $10 million. However this prize money is paid at the rate of $500,000 each year (with the first payment being immediate) for a total of 20 payments. What is the present value of this prize at 10% interest compounded annually? Report your answer in millions, rounded to 2 decimal places.
'''
def qs1():
    print '%5.2f' % calcPV(0.5,20,1.1)


'''
Sunk Costs (Exercise 2.6 in Luenberger): Part I

Questions 2 and 3 are two parts of one problem.

A young couple has already put down a deposit of the first month's rent (equal to $1,000) on a 6-month apartment lease, but have still not paid the first month's rent. The deposit is refundable at the end of six months if they take the apartment. The next day the couple finds a different apartment that they like just as well, but its monthly rent is only $900. And they would again have to put down a deposit of $900 refundable at the end of 6 months. The couple wants to decide whether to stay in the $1000 apartment or switch to the cheaper apartment and forego the deposit. They will do so by comparing the present value of the (future) cash flows associated with the two apartment leases.

What is the present value of the (future) cash flows associated with the $1,000 apartment? Assume an interest rate of 12% per month compounded monthly. Round your answer to the nearest integer.

Assume that the rent for each month is paid at the beginning of the month in advance, and the deposit is returned at the end of six months. Also, your answer should turn out to be a negative number since the rent payment is a cash outflow for the couple.
'''
def qs2():
    r = 1.12
    n = 6
    # case 1
    p = 1000.
    pv1 = calcPV(p,n,r)-p/r**n
    print '%5.1f' % -pv1
'''
Sunk Costs (Exercise 2.6 in Luenberger): Part II

Recall the situation described in Question 2 where a couple is deciding between a $1000 apartment and a $900 apartment.

What is the present value of the cash flows associated with the $900 apartment? Assume an interest rate of 12% per month compounded monthly. Round your answer to the nearest integer.

Assume that the rent for each month is paid at the beginning of the month in advance, and the deposit is returned at the end of six months. Also, your answer should turn out to be a negative number since the rent payment is a cash outflow for the couple.
'''
def qs3():
    r = 1.12
    n = 6
    # case 2
    p = 900.
    pv2 = p+calcPV(p,n,r)-p/r**n
    print '%5.1f' % -pv2

'''
Relation between spot and discount rates

Suppose the spot rates for 1 and 2 years are s1=6.3% and s2=6.9% with annual compounding. Recall that in this course interest rates are always quoted on an annual basis unless otherwise specified. What is the discount rate d(0,2)? 
'''
def qs4():
    print '%5.3f' % (1/1.069**2)

'''
Relation between spot and forward rates

Suppose the spot rates for 1 and 2 years are s1=6.3% and s2=6.9% with annual compounding. Recall that in this course interest rates are always quoted on an annual basis unless otherwise specified. What is the forward rate, f1,2 assuming annual compounding? Round your answer to 3 decimal points (in decimal form, not in percentage).
'''
def qs5():
    print '%5.3f' % (1.069**2/1.063-1)

'''
Forward contract on a stock

The current price of a stock is $400 per share and it pays no dividends. Assuming a constant interest rate of 8% per year compounded quarterly, what is the stock's theoretical forward price for delivery in 9 months? Round your answer to 2 decimal points.
'''
def qs6():
    p = 400
    r = 1.02
    n = 3
    print '%6.2f' % (p*r**n)

'''
    Term structure of interest rates and swap valuation
    
    Suppose the current term structure of interest rates, assuming annual compounding, is as follows:
    
    s1	s2	 s3	 s4	s5	 s6
    7.0%	7.3%	7.7%	8.1%	8.4%	8.8%
    
    Recall that interest rates are always quoted on an annual basis unless stated otherwise.
    
    Suppose a 6-year swap with a notional principal of $10 million is being configured. What is the fixed rate of interest that will make the value of the swap equal to zero? Round your answer to 3 decimal points (in decimal form, not in percentage).
'''
def qs7():
    r=[7.,7.3,7.7,8.1,8.4,8.8]
    r = [1+i/100. for i in r]
    d = [calcDis(ir,i+1) for i,ir in enumerate(r)]
    x = (1-d[-1])/sum(d)
    print '%5.3f' % x

if __name__=="__main__":
    qs1()
    qs2()
    qs3()
    qs4()
    qs5()
    qs6()
    qs7()
