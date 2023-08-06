# -*- coding: utf-8 -*-
"""
多目标函数DTLZ1,2,3,4
"""

import numpy as np

# DTLZ1
def DTLZ1(Chrom, M = 3): # M为问题维度，如2维、3维
    x = Chrom.T
    XM = x[M-1:]
    k = x.shape[0] - M + 1
    gx = 100 * (k + np.sum((XM - 0.5) ** 2 - np.cos(20 * np.pi * (XM - 0.5)), 0))
    
    ObjV = (np.array([[]]).T) * np.zeros((1, Chrom.shape[0]))
    ObjV = np.vstack([ObjV, 0.5 * np.cumprod(x[:M-1], 0)[-1] * (1 + gx)])
    for i in range(2, M):
        ObjV = np.vstack([ObjV, 0.5 * np.cumprod(x[: M-i], 0)[-1] * (1 - x[M-i]) * (1 + gx)])
    ObjV = np.vstack([ObjV, 0.5 * (1 - x[0]) * (1 + gx)])
    return ObjV.T

# DTLZ2
def DTLZ2(Chrom, M = 3): # M为问题维度，如2维、3维
    x = Chrom.T
    XM = x[M-1:]
    gx = np.sum((XM - 0.5) ** 2, 0)
    
    ObjV = (np.array([[]]).T) * np.zeros((1, Chrom.shape[0]))
    ObjV = np.vstack([ObjV, np.cumprod((np.cos(x * np.pi / 2))[:M-1], 0)[-1] * (1 + gx)])
    for i in range(2, M):
        ObjV = np.vstack([ObjV, np.cumprod((np.cos(x * np.pi / 2))[: M-i], 0)[-1] * np.sin(x[M-i] * np.pi / 2) * (1 + gx)])
    ObjV = np.vstack([ObjV, np.sin(x[0] * np.pi / 2) * (1 + gx)])
    return ObjV.T

# DTLZ3
def DTLZ3(Chrom, M = 3): # M为问题维度，如2维、3维
    x = Chrom.T
    XM = x[M-1:]
    k = x.shape[0] - M + 1
    gx = 100 * (k + np.sum((XM - 0.5) ** 2 - np.cos(20 * np.pi * (XM - 0.5)), 0))
    
    ObjV = (np.array([[]]).T) * np.zeros((1, Chrom.shape[0]))
    ObjV = np.vstack([ObjV, np.cumprod((np.cos(x * np.pi / 2))[:M-1], 0)[-1] * (1 + gx)])
    for i in range(2, M):
        ObjV = np.vstack([ObjV, np.cumprod((np.cos(x * np.pi / 2))[: M-i], 0)[-1] * np.sin(x[M-i] * np.pi / 2) * (1 + gx)])
    ObjV = np.vstack([ObjV, np.sin(x[0] * np.pi / 2) * (1 + gx)])
    return ObjV.T

# DTLZ4
def DTLZ4(Chrom, M = 3): # M为问题维度，如2维、3维
    x = Chrom.T
    XM = x[M-1:]
    gx = np.sum((XM - 0.5) ** 2, 0)
    a = 100
    
    ObjV = (np.array([[]]).T) * np.zeros((1, Chrom.shape[0]))
    ObjV = np.vstack([ObjV, np.cumprod((np.cos(x ** a * np.pi / 2))[:M-1], 0)[-1] * (1 + gx)])
    for i in range(2, M):
        ObjV = np.vstack([ObjV, np.cumprod((np.cos(x ** a * np.pi / 2))[: M-i], 0)[-1] * np.sin(x[M-i] ** a * np.pi / 2) * (1 + gx)])
    ObjV = np.vstack([ObjV, np.sin(x[0] ** a * np.pi / 2) * (1 + gx)])
    return ObjV.T

