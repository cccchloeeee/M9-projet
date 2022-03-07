# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:20:37 2022

@author: Emeline
"""
import numpy as np

# matrice G
G = np.zeros([60, 60])

# Room1
# wall (ext)
# convection
G[0, 0] = Gcv_LR_w[1]  # convection wall concrete out
# conduction
G[1, 1] = G[2, 2] = Gcd_LR_w_c  # conduction wall concrete
G[3, 3] = G[4, 4] = Gcd_LR_w_i  # conduction wall insulation
G[5, 5] = G[6, 6] = Gcd_LR_w_p  # conduction wall plaster
# convection
G[7, 7] = Gcv_LR_w[0]  # convection wall plaster inside

# floor
# convection
G[8, 8] = Gcv_LR_f[0]  # convection floor temp fix
# conduction
G[9, 9] = G[10, 10] = Gcd_LR_f  # conduction floor
# convection
G[11, 11] = Gcv_LR_f[0]  # convection floor inside

# door
# convection
G[12, 12] = Gcv_LR_d[0]  # convection door temp fix
# conduction
G[13, 13] = G[14, 14] = Gcd_LR_d  # conduction door
# convection
G[15, 15] = Gcv_LR_d[0]  # convection door inside

# dividing wall
# convection
G[16, 16] = Gcv_LR_dw[0]  # convection d-wall plaster fix
# conduction
G[17, 17] = G[18, 18] = Gcd_LR_dw_p  # conduction d-wall plaster
G[19, 19] = G[20, 20] = Gcd_LR_dw_i  # conduction d-wall insulation
G[21, 21] = G[22, 22] = Gcd_LR_dw_p  # conduction d-wall plaster
# convection
G[23, 23] = Gcv_LR_dw[0]  # convection wall plaster inside

# window + ventilation
# conduction
G[24, 24] = Gw_LR + Gv_LR  # conduction w + venti

# renouvellement air
# conduction
G[25, 25] = Gr_LR  # renouv air LR

# partition wall
# convection
G[26, 26] = Gcv_LRBR_dw[0]  # convection d-wall plaster in
# conduction
G[27, 27] = G[28, 28] = Gcd_LRBR_dw_p  # conduction d-wall plaster
G[29, 29] = G[30, 30] = Gcd_LRBR_dw_i  # conduction d-wall insulation
G[31, 31] = G[32, 32] = Gcd_LRBR_dw_p  # conduction d-wall plaster
# convection
G[33, 33] = Gcv_LRBR_dw[0]  # convection wall plaster inside

# door
# convection
G[34, 34] = Gcv_LRBR_d[0]  # convection door temp fix
# conduction
G[35, 35] = G[36, 36] = Gcd_LRBR_d  # conduction door
# convection
G[37, 37] = Gcv_LRBR_d[0]  # convection door inside

# Room2
# wall (ext)
# convection
G[45, 45] = Gcv_BR_w[1]  # convection wall concrete out
# conduction
G[44, 44] = G[43, 43] = Gcd_BR_w_c  # conduction wall concrete
G[42, 42] = G[41, 41] = Gcd_BR_w_i  # conduction wall insulation
G[40, 40] = G[39, 39] = Gcd_BR_w_p  # conduction wall plaster
# convection
G[38, 38] = Gcv_BR_w[1]  # convection wall plaster inside

# floor
# convection
G[49, 49] = Gcv_BR_f[0]  # convection floor temp fix
# conduction
G[48, 48] = G[47, 47] = Gcd_BR_f  # conduction floor
# convection
G[46, 46] = Gcv_BR_f[0]  # convection floor inside

# dividing wall
# convection
G[57, 57] = Gcv_BR_dw[0]  # convection d-wall plaster fix
# conduction
G[56, 56] = G[55, 55] = Gcd_BR_dw_p  # conduction d-wall plaster
G[54, 54] = G[53, 53] = Gcd_BR_dw_i  # conduction d-wall insulation
G[52, 52] = G[51, 51] = Gcd_BR_dw_p  # conduction d-wall plaster
# convection
G[50, 50] = Gcv_BR_dw[0]  # convection wall plaster inside

# window + ventilation
# conduction
G[59, 59] = Gw_BR + Gv_BR  # conduction w + venti

# renouvellement air
# conduction
G[58, 58] = Gr_BR  # renouv air BR

np.set_printoptions(suppress=False)
print(G)
