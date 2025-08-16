# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:54:31 2024

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
 
def find_range(array, value):
    # Use numpy's searchsorted to find the index where the target value should be inserted
    index = np.searchsorted(array[:,2], value, side='left')
 
    # Use numpy's searchsorted again to find the index where the target value should be inserted for the upper bound
    # end_index = np.searchsorted(array[:,0], end_value, side='right')
 
    return index
 
def check_intersection(point1, point2, need_check):
    u1, v1, n = point1
    u2, v2, n = point2
 
    # Calculate the equation of the line connecting the two points (y = mx + b)
    m = (u2 - u1) / (v2 - v1)
    if m<0:
        return 0
    b = u1 - m * v1
    # print(m)
    # print(b)
    if need_check:
        if (1-b)/(1+m)>bdx[0] and (1-b)/(1+m)<bdx[1]:            
            return 0
    return 1  # No intersection
 
V = 1*1

its = 10
for K in [50]: 
    eps = 0.1
    rho = K/eps
    ac_lst = []
    for l in range(its):
        N = np.random.poisson(rho*V)
        arr = np.random.rand(N,2) #sprinkle in box 
        arr2 = []
        for i in range(N):
            if not (arr[i][0]>bdt[0] and arr[i][0]<bdt[1] and arr[i][1]>bdx[0] and arr[i][1]<bdx[1]):
                arr2.append(arr[i])
        arr2 = np.array(arr2)
        N = len(arr2)
        arr = np.zeros((N,3))
        arr[:,2] = arr2[:,0]+arr2[:,1]
        arr[:,0] = arr2[:,0]
        arr[:,1] = arr2[:,1]
        arr = arr[arr[:, 2].argsort()] #sort by u+v coordinate
        index = find_range(arr,1)

        relations = np.zeros([N,N])
        for i in range(index):
            for j in range(i+1,index):
                relations[i,j] = check_intersection(arr[i], arr[j], False)
            for j in range(index,N):
                relations[i,j] = check_intersection(arr[i], arr[j], True)        
        for i in range(index,N):
            for j in range(i+1,N):
                relations[i,j] = check_intersection(arr[i], arr[j], False)        
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
    # np.savetxt('/rds/general/user/rl1320/home/sprinkling/2d_iso_hole_K'+str(K)+str(datetime.datetime.now())+'.csv',ac_lst,delimiter=',')