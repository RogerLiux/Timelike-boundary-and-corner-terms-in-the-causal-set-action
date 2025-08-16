# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 15:05:39 2024

@author: rl1320
"""


import numpy as np
import matplotlib.pyplot as plt
import scipy.special as scp
import datetime

print(datetime.datetime.now())

bdt = [0.4,0.6]
bdx = [0.4,0.6]

def f2(n,eps):
      return (1-eps)**n - 2*n*eps*(1-eps)**(n-1) + scp.binom(n,2)*eps**2*(1-eps)**(n-2)


def organise_lst_step1(arr):
    for i in range(len(arr)):
        t,x=arr[i][0],arr[i][1]
        if t<bdt[0]:
            if t+x<bdt[0]+bdx[0]:
                if t-x<bdt[0]-bdx[1]:
                    lst1[i]=1
            else:
                if t-x>bdt[0]-bdx[1]:
                    lst4[i]=1
        if t>bdt[1]:
            if t+x<bdt[1]+bdx[1]:
                if t-x<bdt[1]-bdx[0]:
                    lst5[i]=1
            else:
                if t-x>bdt[1]-bdx[0]:
                    lst6[i]=1

def organise_lst_step2(arr):
    testlst=np.ones(N)-lst1-lst4-lst5-lst6
    for i in range(len(testlst)):
        if testlst[i]==1:
            if arr[i][1]>0.5:
                lst3[i]=1 
            else:
                lst2[i]=1
        
def grad(i,j):
    return abs((arr[j][0]-arr[i][0])/(arr[j][1]-arr[i][1]))

V = 1*1

its = 1
action_mean_lst = []
action_err_lst = []
for K in [50]: 
    eps = 0.1
    rho = K/eps
    action_lst = []
    for l in range(its):
        N = np.random.poisson(rho*V)
        arr = np.random.rand(N,2) #sprinkle in box 
        arr2 = []
        for i in range(N):
            if not (arr[i][0]>bdt[0] and arr[i][0]<bdt[1] and arr[i][1]>bdx[0] and arr[i][1]<bdx[1]):
                arr2.append(arr[i])
        arr2 = np.array(arr2)
        arr = arr2[arr2[:, 0].argsort()] #sort by time coordinate
        
        N = len(arr)
        
        lst1 = np.zeros(N)
        lst2 = np.zeros(N)
        lst3 = np.zeros(N)
        lst4 = np.zeros(N)
        lst5 = np.zeros(N)
        lst6 = np.zeros(N)
        
        organise_lst_step1(arr)
        organise_lst_step2(arr)
        
        relations = np.zeros([N,N])
        
        for i in range(N):
            for j in range(i+1,N):
                if lst1[i]==1:
                    if lst5[j]==0 and grad(i,j)>1:
                        relations[i,j] = 1
                elif lst2[i]==1:
                    if (lst2[j]==1 or lst4[j]==1 or lst6[j]==1) and grad(i,j)>1:
                        relations[i,j] = 1
                elif lst3[i]==1:
                    if (lst3[j]==1 or lst4[j]==1 or lst6[j]==1) and grad(i,j)>1:
                        relations[i,j] = 1
                elif lst4[i]==1:
                    if (lst4[j]==1) and grad(i,j)>1:
                        relations[i,j] = 1
                elif lst5[i]==1:
                    if (lst2[j]==1 or lst3[j]==1 or lst5[j]==1 or lst6[j]==1) and grad(i,j)>1:
                        relations[i,j] = 1
                else:
                    if (lst6[j]==1) and grad(i,j)>1:
                        relations[i,j] = 1

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
        action_lst.append(2*(eps*N - 2*(eps**2)*sums))
    np.savetxt('/rds/general/user/rl1320/home/sprinkling/2ddiaholeK'+str(K)+str(datetime.datetime.now())+'.csv',action_lst,delimiter=',')


print(datetime.datetime.now())