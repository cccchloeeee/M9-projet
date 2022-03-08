#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 11:29:39 2022

@author: chloechallamel

Code pour le projet M9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dm4bem


# Physical values
# ===============
# P-controler gain
# ----------------
# Kp = 1e4            # Kp -> ∞ : almost perfect controller
Kp = 1e-3         # Kp -> 0 : no controller Kp -> 0
Kp

# Dimensions & surface areas
# --------------------------
l = 4               # m largeur du studio
L = 8               # m longueur du studio
H = 2.5             # m hauteur du studio

# Air-flow rate
# -------------
Va_livingroom = 6 * 4 * 2.5        # m³ volume of air  in the living room
Va_bathroom = 2 * 4 * 2.5          # m³ volume of air  in the bathroom
ACH = 1             # air changes per hour
Va_livingroom_dot = ACH * Va_livingroom / 3600    # m³/s air infiltration
Va_bathroom_dot = ACH * Va_bathroom / 3600

# Thermophyscal properties
# ------------------------
air = {'Density': 1.2,                      # kg/m³
       'Specific heat': 1000}               # J/kg.K

# Valeurs récupérées de DB
materials = {'Conductivity': [2.3, 0.0457, 0.25, 0.19, 1.4],   # W/m.K
             'Density': [2300, 40, 2800, 700, 2100],           # kg/m³
             'Specific heat': [1000, 1450, 896, 2390, 840],    # J/kg.K
             'Width': [0.3, 0.05, 0.013, 0.035, 0.1],          # m
             'Slice': [1, 1, 1, 1, 1]}                         # nb of meshes
materials = pd.DataFrame(
    materials, index=['Concrete', 'Insulation', 'Plaster', 'Door',
                      'Floor'])

# Surfaces
surfaces = {'LR': [13.11, 18.4, 6.6, 1.89, 48],      # m²
            'BR': [15, 3.8, 1.2, 0, 16],
            'LR-BR': [8.11, 0, 0, 1.89, 0]}
surfaces = pd.DataFrame(
    surfaces, index=['Dividingwall', 'Wall', 'Window', 'Door', 'Floor'])

# convection coefficients, W/m² K
h = pd.DataFrame([{'in': 4., 'out': 10}])


# Thermal circuit (EN COURS DE MODIF)
# ===============

# Thermal conductances
# --------------------
# Conduction
# Conduction zone 1 : LR
#            in wall
Gcd_LR_w_c = materials['Conductivity']['Concrete'] / \
    materials['Width']['Concrete'] * surfaces['LR']['Wall']

Gcd_LR_w_i = materials['Conductivity']['Insulation'] / \
    materials['Width']['Insulation'] * surfaces['LR']['Wall']

Gcd_LR_w_p = materials['Conductivity']['Plaster'] / \
    materials['Width']['Plaster'] * surfaces['LR']['Wall']

#            in dividing wall
Gcd_LR_dw_p = materials['Conductivity']['Plaster'] / \
    materials['Width']['Plaster'] * surfaces['LR']['Dividingwall']

Gcd_LR_dw_i = materials['Conductivity']['Insulation'] / \
    materials['Width']['Insulation'] * surfaces['LR']['Dividingwall']

#           door
Gcd_LR_d = materials['Conductivity']['Door'] / \
    materials['Width']['Door'] * surfaces['LR']['Door']

#           floor
Gcd_LR_f = materials['Conductivity']['Floor'] / \
    materials['Width']['Floor'] * surfaces['LR']['Floor']

# Conduction zone 2 : BR
#            in wall
Gcd_BR_w_c = materials['Conductivity']['Concrete'] / \
    materials['Width']['Concrete'] * surfaces['BR']['Wall']

Gcd_BR_w_i = materials['Conductivity']['Insulation'] / \
    materials['Width']['Insulation'] * surfaces['BR']['Wall']

Gcd_BR_w_p = materials['Conductivity']['Plaster'] / \
    materials['Width']['Plaster'] * surfaces['BR']['Wall']

#            in dividing wall
Gcd_BR_dw_p = materials['Conductivity']['Plaster'] / \
    materials['Width']['Plaster'] * surfaces['BR']['Dividingwall']

Gcd_BR_dw_i = materials['Conductivity']['Insulation'] / \
    materials['Width']['Insulation'] * surfaces['BR']['Dividingwall']

#           floor
Gcd_BR_f = materials['Conductivity']['Floor'] / \
    materials['Width']['Floor'] * surfaces['BR']['Floor']

# Conduction zone 3 : LR-BR
#            in dividing wall
Gcd_LRBR_dw_p = materials['Conductivity']['Plaster'] / \
    materials['Width']['Plaster'] * surfaces['LR-BR']['Dividingwall']

Gcd_LRBR_dw_i = materials['Conductivity']['Insulation'] / \
    materials['Width']['Insulation'] * surfaces['LR-BR']['Dividingwall']

#           door
Gcd_LRBR_d = materials['Conductivity']['Door'] / \
    materials['Width']['Door'] * surfaces['LR-BR']['Door']

# Convection
# Convection zone 1 : LR
Gcv_LR_w = h * surfaces['LR']['Wall']               # in wall

Gcv_LR_dw = h * surfaces['LR']['Dividingwall']      # in in dividing wall

Gcv_LR_d = h * surfaces['LR']['Door']               # door

Gcv_LR_f = h * surfaces['LR']['Floor']              # floor

# Convection zone 2 : BR
Gcv_BR_w = h * surfaces['BR']['Wall']               # in wall

Gcv_BR_dw = h * surfaces['BR']['Dividingwall']      # in in dividing wall

Gcv_BR_f = h * surfaces['BR']['Floor']              # floor

# Convection zone 3 : LR-BR
Gcv_LRBR_dw = h * surfaces['LR-BR']['Dividingwall']   # in in dividing wall

Gcv_LRBR_d = h * surfaces['LR-BR']['Door']           # door

# Ventilation & advection
Gv_LR = Va_livingroom_dot * air['Density'] * air['Specific heat']

Gv_BR = Va_bathroom * air['Density'] * air['Specific heat']

# Window : conductance Uw * S
Uw = 1.96   # W/(m2.K) pour double-vitrage selon DB

Gw_LR = Uw * surfaces['LR']['Window']

Gw_BR = Uw * surfaces['BR']['Window']

# Renouvellement d'air
Gr_LR = Gr_BR = Kp


# Thermal capacities
# ------------------
# zone 1 : LR
C_LR_w_c = materials['Density']['Concrete'] * \
    materials['Specific heat']['Concrete'] * \
    surfaces['LR']['Wall'] * materials['Width']['Concrete']

C_LR_w_i = materials['Density']['Insulation'] * \
    materials['Specific heat']['Insulation'] * \
    surfaces['LR']['Wall'] * materials['Width']['Insulation']

C_LR_w_p = materials['Density']['Plaster'] * \
    materials['Specific heat']['Plaster'] * \
    surfaces['LR']['Wall'] * materials['Width']['Plaster']

C_LR_dw_p = materials['Density']['Plaster'] * \
    materials['Specific heat']['Plaster'] * \
    surfaces['LR']['Dividingwall'] * materials['Width']['Plaster']

C_LR_dw_i = materials['Density']['Insulation'] * \
    materials['Specific heat']['Insulation'] * \
    surfaces['LR']['Dividingwall'] * materials['Width']['Insulation']

C_LR_d = materials['Density']['Door'] * \
    materials['Specific heat']['Door'] * \
    surfaces['LR']['Door'] * materials['Width']['Door']

C_LR_f = materials['Density']['Floor'] * \
    materials['Specific heat']['Floor'] * \
    surfaces['LR']['Floor'] * materials['Width']['Floor']

# zone 2 : BR
C_BR_w_c = materials['Density']['Concrete'] * \
    materials['Specific heat']['Concrete'] * \
    surfaces['BR']['Wall'] * materials['Width']['Concrete']

C_BR_w_i = materials['Density']['Insulation'] * \
    materials['Specific heat']['Insulation'] * \
    surfaces['BR']['Wall'] * materials['Width']['Insulation']

C_BR_w_p = materials['Density']['Plaster'] * \
    materials['Specific heat']['Plaster'] * \
    surfaces['BR']['Wall'] * materials['Width']['Plaster']

C_BR_dw_p = materials['Density']['Plaster'] * \
    materials['Specific heat']['Plaster'] * \
    surfaces['BR']['Dividingwall'] * materials['Width']['Plaster']

C_BR_dw_i = materials['Density']['Insulation'] * \
    materials['Specific heat']['Insulation'] * \
    surfaces['BR']['Dividingwall'] * materials['Width']['Insulation']

C_BR_f = materials['Density']['Floor'] * \
    materials['Specific heat']['Floor'] * \
    surfaces['BR']['Floor'] * materials['Width']['Floor']

# zone 3 : LR-BR
C_LRBR_dw_p = materials['Density']['Plaster'] * \
    materials['Specific heat']['Plaster'] * \
    surfaces['LR-BR']['Dividingwall'] * materials['Width']['Door']

C_LRBR_dw_i = materials['Density']['Insulation'] * \
    materials['Specific heat']['Insulation'] * \
    surfaces['LR-BR']['Dividingwall'] * materials['Width']['Insulation']

C_LRBR_d = materials['Density']['Door'] * \
    materials['Specific heat']['Door'] * \
    surfaces['LR-BR']['Door'] * materials['Width']['Door']

# air
C_LR_air = air['Density'] * air['Specific heat'] * Va_livingroom

C_BR_air = air['Density'] * air['Specific heat'] * Va_bathroom


# Incidence matrix A
# ------------------
A = np.zeros([60, 49])

# Flux directed to livingroom
A[0,   0] = 1
A[1,   0], A[1,   1] = -1, 1
A[2,   1], A[2,   2] = -1, 1
A[3,   2], A[3,   3] = -1, 1
A[4,   3], A[4,   4] = -1, 1
A[5,   4], A[5,   5] = -1, 1
A[6,   5], A[6,   6] = -1, 1
A[7,   6], A[7,  20] = -1, 1
A[8,   7] = 1
A[9,   7], A[9,   8] = -1, 1
A[10,  8], A[10,  9] = -1, 1
A[11,  9], A[11, 20] = -1, 1
A[12, 10] = 1
A[13, 10], A[13, 11] = -1, 1
A[14, 11], A[14, 12] = -1, 1
A[15, 12], A[15, 20] = -1, 1
A[16, 13] = 1
A[17, 13], A[17, 14] = -1, 1
A[18, 14], A[18, 15] = -1, 1
A[19, 15], A[19, 16] = -1, 1
A[20, 16], A[20, 17] = -1, 1
A[21, 17], A[21, 18] = -1, 1
A[22, 18], A[22, 19] = -1, 1
A[23, 19], A[23, 20] = -1, 1
A[24, 20] = 1
A[25, 20] = 1
A[26, 20], A[26, 21] = -1, 1
A[27, 21], A[27, 22] = -1, 1
A[28, 22], A[28, 23] = -1, 1
A[29, 23], A[29, 24] = -1, 1
A[30, 24], A[30, 25] = -1, 1
A[31, 25], A[31, 26] = -1, 1
A[32, 26], A[32, 27] = -1, 1
A[33, 27], A[33, 31] = -1, 1
A[34, 28] = 1
A[35, 28], A[35, 29] = -1, 1
A[36, 29], A[36, 30] = -1, 1
A[37, 30], A[37, 31] = -1, 1

# Flux directed to bathroom
A[38, 31], A[38, 32] = 1, -1
A[39, 32], A[39, 33] = 1, -1
A[40, 33], A[40, 34] = 1, -1
A[41, 34], A[41, 35] = 1, -1
A[42, 35], A[42, 36] = 1, -1
A[43, 36], A[43, 37] = 1, -1
A[44, 37], A[44, 38] = 1, -1
A[45, 38] = 1
A[46, 31], A[46, 39] = 1, -1
A[47, 39], A[47, 40] = 1, -1
A[48, 40], A[48, 41] = 1, -1
A[49, 41] = 1
A[50, 31], A[50, 42] = 1, -1
A[51, 42], A[51, 43] = 1, -1
A[52, 43], A[52, 44] = 1, -1
A[53, 44], A[53, 45] = 1, -1
A[54, 45], A[54, 46] = 1, -1
A[55, 46], A[55, 47] = 1, -1
A[56, 47], A[56, 48] = 1, -1
A[57, 48] = 1
A[58, 31] = 1
A[59, 31] = 1

# Conductance matrix G
# --------------------
G = np.zeros([60, 60])

# Livingroom
# wall (ext)
# convection
G[0, 0] = Gcv_LR_w['out']  # convection wall concrete out
# conduction
G[1, 1] = G[2, 2] = Gcd_LR_w_c  # conduction wall concrete
G[3, 3] = G[4, 4] = Gcd_LR_w_i  # conduction wall insulation
G[5, 5] = G[6, 6] = Gcd_LR_w_p  # conduction wall plaster
# convection
G[7, 7] = Gcv_LR_w['in']  # convection wall plaster inside

# floor
# convection
G[8, 8] = Gcv_LR_f['in']  # convection floor temp fix
# conduction
G[9, 9] = G[10, 10] = Gcd_LR_f  # conduction floor
# convection
G[11, 11] = Gcv_LR_f['in']  # convection floor inside

# door
# convection
G[12, 12] = Gcv_LR_d['in']  # convection door temp fix
# conduction
G[13, 13] = G[14, 14] = Gcd_LR_d  # conduction door
# convection
G[15, 15] = Gcv_LR_d['in']  # convection door inside

# dividing wall
# convection
G[16, 16] = Gcv_LR_dw['in']  # convection d-wall plaster fix
# conduction
G[17, 17] = G[18, 18] = Gcd_LR_dw_p  # conduction d-wall plaster
G[19, 19] = G[20, 20] = Gcd_LR_dw_i  # conduction d-wall insulation
G[21, 21] = G[22, 22] = Gcd_LR_dw_p  # conduction d-wall plaster
# convection
G[23, 23] = Gcv_LR_dw['in']  # convection wall plaster inside

# window + ventilation
# conduction
G[24, 24] = Gw_LR + Gv_LR  # conduction w + venti

# renouvellement air
# conduction
G[25, 25] = Gr_LR  # renouv air LR

# partition wall
# convection
G[26, 26] = Gcv_LRBR_dw['in']  # convection d-wall plaster in
# conduction
G[27, 27] = G[28, 28] = Gcd_LRBR_dw_p  # conduction d-wall plaster
G[29, 29] = G[30, 30] = Gcd_LRBR_dw_i  # conduction d-wall insulation
G[31, 31] = G[32, 32] = Gcd_LRBR_dw_p  # conduction d-wall plaster
# convection
G[33, 33] = Gcv_LRBR_dw['in']  # convection wall plaster inside

# door
# convection
G[34, 34] = Gcv_LRBR_d['in']  # convection door temp fix
# conduction
G[35, 35] = G[36, 36] = Gcd_LRBR_d  # conduction door
# convection
G[37, 37] = Gcv_LRBR_d['in']  # convection door inside

# Bathroom
# wall (ext)
# convection
G[45, 45] = Gcv_BR_w['out']  # convection wall concrete out
# conduction
G[44, 44] = G[43, 43] = Gcd_BR_w_c  # conduction wall concrete
G[42, 42] = G[41, 41] = Gcd_BR_w_i  # conduction wall insulation
G[40, 40] = G[39, 39] = Gcd_BR_w_p  # conduction wall plaster
# convection
G[38, 38] = Gcv_BR_w['in']  # convection wall plaster inside

# floor
# convection
G[49, 49] = Gcv_BR_f['in']  # convection floor temp fix
# conduction
G[48, 48] = G[47, 47] = Gcd_BR_f  # conduction floor
# convection
G[46, 46] = Gcv_BR_f['in']  # convection floor inside

# dividing wall
# convection
G[57, 57] = Gcv_BR_dw['in']  # convection d-wall plaster fix
# conduction
G[56, 56] = G[55, 55] = Gcd_BR_dw_p  # conduction d-wall plaster
G[54, 54] = G[53, 53] = Gcd_BR_dw_i  # conduction d-wall insulation
G[52, 52] = G[51, 51] = Gcd_BR_dw_p  # conduction d-wall plaster
# convection
G[50, 50] = Gcv_BR_dw['in']  # convection wall plaster inside

# window + ventilation
# conduction
G[59, 59] = Gw_BR + Gv_BR  # conduction w + venti

# renouvellement air
# conduction
G[58, 58] = Gr_BR  # renouv air BR


# Capacity matrix C
# -----------------
C = np.zeros([49, 49])

C_BR_air = C_BR_dw_i = C_BR_w_i = C_LR_dw_i = C_LRBR_dw_i = 0
# C_BR_air = C_BR_dw_i = C_BR_w_i = C_LR_air = C_LR_dw_i = C_LR_w_i = C_LRBR_dw_i = 0

# Livingroom : LR
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

# Bathroom
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

# Vector of temperature sources b
# -------------------------------
b = np.zeros(60)
b[[0, 8, 12, 16, 24, 25, 45, 49, 57, 58, 59]] = 1

# Vector of heat sources f
# ------------------------
f = np.zeros(49)
f[[0, 6, 8, 19, 20, 21, 27, 31, 32, 38, 40, 42]] = 1

# Vector of outputs
# -----------------
y = np.zeros(49)  # 1 si on veut que la T sorte, 0 sinon
y[[20, 31]] = 1

# Input vector
# ------------
u = np.hstack([b[np.nonzero(b)], f[np.nonzero(f)]])


# Thermal circuit -> state-space
# ==============================
[As, Bs, Cs, Ds] = dm4bem.tc2ss(A, G, b, C, f, y)

# Maximum time-step
dtmax = min(-2. / np.linalg.eig(As)[0])
print(f'Maximum time step: {dtmax:.2f} s')
# dt = 5
dt = 360
print(f'Time step: {dt:.2f} s')

# Step response
# -------------
duration = 3600 * 24 * 2        # [s]
# number of steps
n = int(np.floor(duration / dt))

t = np.arange(0, n * dt, dt)    # time vector

# Vectors of state and input (in time)
n_tC = As.shape[0]              # no of state variables (temps with capacity)
# u = [To To To Tsp Phio Phii Qaux Phia]
u = np.zeros([23, n])
u[[0, 2, 4, 6, 8, 10]] = 1
# u[0, 0] = u[2, 0] = u[4, 0] = u[6, 0] = u[8, 0] = u[10, 0] = 1

u = np.zeros([8, n])
u[0:3, :] = np.ones([3, n])

# initial values for temperatures obtained by explicit and implicit Euler
temp_exp = np.zeros([n_tC, t.shape[0]])
temp_imp = np.zeros([n_tC, t.shape[0]])

I = np.eye(n_tC)
for k in range(n - 1):
    temp_exp[:, k + 1] = (I + dt * As) @\
        temp_exp[:, k] + dt * Bs @ u[:, k]
    temp_imp[:, k + 1] = np.linalg.inv(I - dt * As) @\
        (temp_imp[:, k] + dt * Bs @ u[:, k])

y_exp = Cs @ temp_exp + Ds @  u
y_imp = Cs @ temp_imp + Ds @  u

fig, axs = plt.subplots(3, 1)
axs[0].plot(t / 3600, y_exp[1].T, t / 3600, y_imp[1].T)
axs[0].set(xlabel='Time [h]', ylabel='$T_i$ [°C]',
           title='Step input: To = 1°C')
plt.show()


# Simulation with weather data
# ----------------------------
