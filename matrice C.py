# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 16:29:17 2022

@author: Emeline
"""
import numpy as np

# matrice C
C = np.zeros([49, 49])

# Room1 : LR
# wall (ext)
C[1, 1] = C_LR_w_c
C[3, 3] = C_LR_w_i
C[5, 5] = C_LR_w_p
# floor
C[8, 8] = C_LR_f
# dividingwall
C[14, 14] = C[18, 18] = C_LR_dw_p
C[16, 16] = C_LR_dw_i
# door
C[11, 11] = C_LR_d
# air
C[20, 20] = C_LR_air


# Partition wall : LR-BR
# dividingwall
C[22, 22] = C[26, 26] = C_LRBR_dw_p
C[24, 24] = C_LRBR_dw_i
# door
C[29, 29] = C_LRBR_d

# Room2
# wall (ext)
C[37, 37] = C_BR_w_c
C[35, 35] = C_BR_w_i
C[33, 33] = C_BR_w_p
# floor
C[40, 40] = C_BR_f
# dividingwall
C[47, 47] = C[43, 43] = C_BR_dw_p
C[45, 45] = C_BR_dw_i
# air
C[31, 31] = C_BR_air

np.set_printoptions(suppress=False)
print(C)
