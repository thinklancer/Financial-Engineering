import sys
import os
import numpy as np

def plotTree(filename,data):
    n = len(data)
    with open(filename+'.dot','w') as f:
        f.write("digraph tree{\n")
        f.write("    rankdir=LR;")
        for i in range(n):
            for j in range(i+1):
                if i==0:
                    line = '    node'+str(i)+str(j)+';\n'
                else:
                    if j==0:
                        line = '    node'+str(i-1)+str(j)+'-> node'+str(i)+str(j)+';\n'
                    if j==i:
                        line = '    node'+str(i-1)+str(j-1)+'-> node'+str(i)+str(j)+';\n'
                    if j!=0 and j!=i:
                        line = '    node'+str(i-1)+str(j)+'-> node'+str(i)+str(j)+';\n'
                        line += '    node'+str(i-1)+str(j-1)+'-> node'+str(i)+str(j)+';\n'
                f.write(line)
        for i in range(n):
            levelline=''
            for j in range(i+1):
                line = '    node'+str(i)+str(j)+'[label = "'+str(data[i,j])+'"];\n'
                f.write(line)
                levelline += 'node'+str(i)+str(j)+' '
            line = '    {rank=same; '+levelline+'}\n'
            f.write(line)
        f.write('}')
    os.system("dot -Tps "+filename+".dot -o temp.ps")
    os.system("ps2pdf temp.ps")
    os.system("mv temp.pdf "+filename+".pdf")

if __name__ == "__main__":
    data = np.random.randint(5,size=(4,4))
    plotTree('test',data)


