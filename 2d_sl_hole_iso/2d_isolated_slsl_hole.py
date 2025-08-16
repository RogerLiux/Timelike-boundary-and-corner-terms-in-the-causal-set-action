# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.special as scp
import datetime
 
print(datetime.datetime.now())
 
bdu = [0.2,0.8]
bdv = [0.2,0.8]
 
def f2(n,eps):
      return (1-eps)**n - 2*n*eps*(1-eps)**(n-1) + scp.binom(n,2)*eps**2*(1-eps)**(n-2)
 
V = 1*1

its = 100
for K in [70]:#,100,200,300,400,600,800]: 
    eps = 0.1
    rho = K/eps
    ac_lst = []
    for l in range(its):
        N = np.random.poisson(rho*V)
        arr = np.random.rand(N,2) #sprinkle in box 
        arr2 = []
        for i in range(N):
            if not (arr[i][0]>-2*arr[i][1]+1.2 and arr[i][0]>-1/2*arr[i][1]+0.6 and arr[i][0]<-2*arr[i][1]+1.8 and arr[i][0]<-1/2*arr[i][1]+0.9):
                arr2.append(arr[i])
        arr2 = np.array(arr2)
        N = len(arr2)
        arr = arr2[arr2[:, 0].argsort()] 
        relations = np.zeros([N,N])
        
        lst1 = np.zeros(N)
        lst2 = np.zeros(N)
        lst3 = np.zeros(N)
        lst4 = np.zeros(N)
        lst5 = np.zeros(N)
        lst6 = np.zeros(N)
        
        for i in range(N):
            if bdu[0] < arr[i][0] and arr[i][0] < bdu[1] :
                if arr[i][1] < bdv[0]:
                    lst5[i]=1
                elif arr[i][1] > bdv[1]:
                    lst6[i]=1
                elif arr[i][0]+arr[i][1]>1:
                    lst2[i]=1
                else:
                    lst1[i]=1
            if bdv[0] < arr[i][1] and arr[i][1] < bdv[1] :
                if arr[i][0] < bdu[0]:
                    lst3[i]=1
                elif arr[i][0] > bdu[1]:
                    lst4[i]=1
        
        for i in range(N):
            for j in range(i+1,N):
                if arr[i][1] < arr[j][1]:
                    relations[i,j] = 1   
                if (lst1[i]==1 and lst1[j]==0) or (lst2[i]==0 and lst2[j]==1):
                    relations[i,j] = 0
                if lst3[i]==1 and lst4[j]==1:
                    relations[i,j] = 0
                if lst5[i]==1 and lst6[j]==1:
                    relations[i,j] = 0
        sums = 0
        for x in range(N):
            causal_past = []
            for y in range(x):
                if relations[y,x] == 1:
                    causal_past.append(y)
            yindex = 0
            for y in causal_past:
                n_count = 0
                for z in causal_past[yindex:]:
                    n_count += relations[y,z]
                sums += f2(n_count,eps)
                yindex += 1
        ac_lst.append(2*(eps*N - 2*(eps**2)*sums))
        print(datetime.datetime.now())
    np.savetxt('/rds/general/user/rl1320/home/sprinkling/2d_iso_slsl_hole_K'+str(K)+str(datetime.datetime.now())+'.csv',ac_lst,delimiter=',')
