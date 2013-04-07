'''
Binomial Tree structure
========================================
'''
import numpy as np

class BinomialTree(object):
    ''' Binomial Tree Structure
    '''
    def __init__(self,n):
        '''
        initialize the binomial tree
        
        :param n: number of levels ( equals time step+1)
        :returns: bt binomial tree
        '''
        self.n = n
        self.bt = np.zeros(n*(n+1)/2)

    def getNode(self,i,j):
        '''
        return the value of given node
        
        :param i: at level i
        :param j: at note j in i level
        '''
        return self.bt[i*(i+1)/2+j]

    def setNode(self,i,j,v):
        ''' set the value of given node

        :param i: at level i
        :param j: at note j in i level
        :param v: the assigned value
        '''
        self.bt[i*(i+1)/2+j] = v

    def showData(self,pfile,form='{0:f}',coef=1):
        ''' visualize the data

        :param pfile: opened file pointer
        :param form: set format of output
        :param coef: set the scale factor for output
        '''
        pfile.write('digraph tree{\n   size="10,10";\n ratio=compress;')
        pfile.write("    rankdir=LR; rotate=90\n")
        for i in range(self.n):
            for j in range(i+1):
                if i==0:
                    line = '    node'+str(i)+str(j)+';\n'
                else:
                    if j==0:
                        line = '    node'+str(i-1)+str(j)+'-> node'+str(i)+str(j)+';\n'
                    elif j==i:
                        line = '    node'+str(i-1)+str(j-1)+'-> node'+str(i)+str(j)+';\n'
                    elif j!=0 and j!=i:
                        line = '    node'+str(i-1)+str(j)+'-> node'+str(i)+str(j)+';\n'
                        line += '    node'+str(i-1)+str(j-1)+'-> node'+str(i)+str(j)+';\n'
                pfile.write(line)
        for i in range(self.n):
            levelline=''
            for j in range(i+1):
                line = '    node'+str(i)+str(j)+'[label = "'+form.format(self.getNode(i,j)*coef)+'"];\n'
                pfile.write(line)
                levelline += 'node'+str(i)+str(j)+' '
            line = '    {rank=same; '+levelline+'}\n'
            pfile.write(line)
        pfile.write('}')

