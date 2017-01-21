from numpy import *
from numpy import linalg as la

def filetoMat(filename):
    fl = open(filename)
    arry = fl.readlines()
    rMat = zeros((943,1682))
    classLabel = []
    for lines in arry:
        lines = lines.strip()
        ll = lines.split('\t')
        rMat[int(ll[0])-1,int(ll[1])-1] = int(ll[2])
    return rMat

def cosSim(inX,inY):
    num = float(inX.T*inY)
    denom = la.norm(inX)*la.norm(inY)
    return 0.5 +0.5*(num/denom)

def simMat(DataSet,item,user):
    n = shape(DataSet)[1]
    simT=0.0;ratSimT=0.0
    for j in range(n):
        ur = DataSet[user,j]
        if ur==0: continue
        ovl = nonzero(logical_and(DataSet[:,item].A>0, \
                                  DataSet[:,j].A>0))[0]
        if len(ovl) ==0 : sim =0
        else : sim = cosSim(DataSet[ovl,item],DataSet[ovl,j])
        simT += sim
        ratSimT += sim*ur
    if simT ==0 : return 0
    else : return ratSimT/simT
def loadExData():
    return[[4, 4, 0, 2, 2],
           [4, 0, 0, 3, 3],
           [4, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]

def recd(user,DataSet):
    unR = nonzero(DataSet[user,:].A==0)[1]
    if len(unR) ==0: print'U have rated everything'
    else:
        itemscore = []
        for item in unR:
            estS = simMat(DataSet,item,user)
            itemscore.append((item,estS))
        print (sorted(itemscore,key=lambda jj:jj[1],reverse=True))

def MovieData():
    dfl = open('u.item')
    arry = dfl.readlines()
    mfl = open('MovieData.txt','w')
    for line in arry:
        line.strip();
        ls = line.split('|')
        mfl.write(ls[0] +' '+ ls[1]+'\n')
    mfl.close()
def UserData():
    DataSet = matrix(filetoMat('u.data'))
    rows = shape(DataSet)[1]
    fl = open('usrData.txt')
    ll = fl.readlines()
    dMat = zeros((1,rows))
    for a in ll:
        a = a.strip()
        lst = a.split('   ')
        dMat[0,(int(lst[0])-1)] = int(lst[1])
    DataSet = vstack([DataSet,dMat])
    user = shape(DataSet)[0]-1
    recd(user,DataSet)
UserData()