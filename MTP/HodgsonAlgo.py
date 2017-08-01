#Importing all required modules
#****************************************************************
import math	
import random
from copy import deepcopy
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats
import xlwt
import xlrd
#****************************************************************
def EDDrule(data):
    cdata = data[:]
    for a in range(0, len(cdata)):
        if(cdata[a][0]=='dj'):
            index=a
    for i in range (1, len(cdata[0])-1):
        for j in range (i+1, len(cdata[0])):
            if (cdata[index][i] > cdata[index][j]):
                for l in range (0,len(cdata)):
                    z =  cdata[l][i]
                    cdata[l][i] = cdata[l][j]
                    cdata[l][j] = z
    #print "After EDD rule",cdata
    return cdata

def LateCompT(data):
    cdata = data[:]
    comT = []
    lateT =[]
    comT.append('Cj')
    lateT.append('Lj')
    total=0
    for b in range(0, len(cdata)):
        if (cdata[b][0]=='tj'):
            index1=b
        if(cdata[b][0]=='dj'):
            index=b
    for i in range (1,len(cdata[0])):
        total = total + cdata[index1][i]
        comT.append(total)
        if(comT[i]> cdata[index][i]):
            lateT.append(comT[i] -cdata[index][i])
        else:
            lateT.append(0)
    #print "Lateness Time after EDD",lateT
    #print "Completion time after EDD",comT
    return (comT,lateT)

def RmlongTjob(data,lateT):
    cdata = data[:]
    for b in range(0, len(cdata)):
        if (cdata[b][0]=='tj'):
            index1=b
        if (cdata[b][0]=='job j'):
            index3=b
    for i in range(1,len(cdata[0])):
        if(lateT[i]>0):
            k=i
            break;
    MaxA=[]
    for i in range(1,k+1):
        MaxA.append(cdata[index1][i])
    print MaxA
    MaxTj=max(MaxA)
    for j in range(1,k+1):
            if(cdata[index1][j]==MaxTj):
                indexTj=j
                SetAvalue = cdata[index3][j]
    shiftL=[]
    for b in range(0,len(cdata)):
        shiftL.append(cdata[b][indexTj])
    print "Values to be shifted", shiftL
    for i in range(0,len(cdata)):
        m=indexTj
        for j in range(1,len(cdata[0])-1):
            if (j >= m):
                cdata[i][m]=cdata[i][j+1]
                m=m+1
        cdata[i][m]=shiftL[i]

    #print MaxTj
    #print indexTj
    #print cdata
    print SetAvalue
    return (MaxTj,indexTj,cdata,SetAvalue)

def hodgson():
    workbook = xlrd.open_workbook('ExampleBook.xlsx')
    sheet = workbook.sheet_by_index(0)

    #r = sheet.row(0) #returns all the CELLS of row 0,
    #c = sheet.col_values(0) #returns all the VALUES of row 0,

    r = sheet.nrows
    c = sheet.ncols

    rdata = [] #make a data store
    for i in range(0,sheet.nrows):
      rdata.append(sheet.row_values(i)) #drop all the values in the rows into data

    cdata = [] #make a data store
    for j in range(0,sheet.ncols):
      cdata.append(sheet.col_values(j)) #drop all the values in the rows into data
    print rdata
    print cdata
    count = 0
    edd_seq = EDDrule(cdata)
    print "EDD",edd_seq
    myComp, mylate = LateCompT(cdata)
    print "Lateness",mylate
    print "Completion",myComp
    for i in range(1,len(mylate)):
        if(mylate[i]>0):
            count += 1
    if(count >1):
        for i1 in range(0, len(cdata)):
            if(cdata[i1][0]=='job j'):
                index2=i1
        setA = []
        setB = []
        setB = cdata[index2][1:]
        print setB,setA
        mdata = (cdata[:]
        print mdata
        signal = True

        for c in range(0,3):
            MAXtj,IndexTj, cdata, setAvalue= RmlongTjob(cdata,mylate)
            print "max process time",MAXtj
            print "Index of Max_Tj",IndexTj
            print "Updated data",cdata
            myComp, mylate = LateCompT(cdata)
            print "Lateness",mylate
            print "Completion",myComp
            setA.append(setAvalue)
            print "updated set A",setA
            del(setB[IndexTj-1])
            print "updated set B",setB
            
            for j1 in range(1,len(mdata[0])):
                 if(mdata[index2][j1]== setAvalue):
                     for j2 in range(0, len(mdata)):
                         del(mdata[j2][j1])
            print mdata
                    
                
            
            
            
            
        
    
