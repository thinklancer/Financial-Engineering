import numpy as np

# default rate of individual portfolio
ppd = np.array([0.2,0.2,0.06,0.3,0.4,0.65,0.3,0.23,0.02,0.12,0.134,0.21,0.08,0.1,0.1,0.02,0.3,0.015,0.2,0.03])

# probability with i credit default
n = len(ppd)

pd = np.zeros(n+1)
pd[0] = 1-ppd[0]
pd[1] = ppd[0]
for i in range(1,n):
    for j in range(i+1,0,-1):
        pd[j] = pd[j-1]*ppd[i] + pd[j]*(1-ppd[i])
    pd[0] = pd[0]*(1-ppd[i])

# question 1
print "%.3f" % pd[3]

# question 2
meandefault = np.sum(np.arange(n+1)*pd)
print "%.2f" % meandefault

# question 3
variancedefault = np.sum((np.arange(n+1)-meandefault)**2*pd)
print "%.2f" % variancedefault

# question 4
loss = np.arange(n+1)
id = np.where(loss > 2)[0]
loss[id] = 2
print  "%.2f" % np.sum(loss*pd)

# question 5
loss = np.arange(n+1)
id = np.where(loss > 4)[0]
loss[id] = 4
loss -= 2
id = np.where(loss < 0)[0]
loss[id] = 0
print  "%.2f" % np.sum(loss*pd)

# question 6
loss = np.arange(n+1)
loss -= 4
id = np.where(loss < 0)[0]
loss[id] = 0
print  "%.2f" % np.sum(loss*pd)
