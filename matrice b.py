# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:18:17 2022

@author: Emeline
"""
import numpy as np

b = np.zeros(60)
b[0] = 1
b[8] = 1
b[16] = 1
b[24] = 1
b[25] = 1
b[45] = 1
b[49] = 1
b[57] = 1
b[58] = 1
b[59] = 1
np.set_printoptions(suppress=False)
# print(b)

b = np.zeros(60)
b[[0, 8, 16, 24, 25, 45, 49, 57, 58, 59]] = 1
# print(b)

# b = np.zeros(60)
# b[[0, 8, 24, 45, 49, 59]] = T0
# b[[16, 57]] = T1
# b[[25]] = T2
# b[[58]] = T3
