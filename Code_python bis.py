#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 11:29:39 2022

@author: chloechallamel

Essai de code pour le projet M9
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import dm4bem


# Physical values
# ===============
# P-controler gain
# ----------------
Kp = 1e4            # Kp -> ∞ : almost perfect controller
# Kp = 1e-3         # Kp -> 0 : no controller Kp -> 0
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

"""From DesignBuilder"""
# VALEURS FLOOR-DOOR-WINDOW A RECUPERER DE DESIGN BUILDER

materials = {'Conductivity': [2.3, 0.0457, 0.25, 0, 0, 0],      # W/m.K
             'Density': [2300, 40, 28000, 0, 0, 0],             # kg/m³
             'Specific heat': [1000, 1450, 896, 0, 0, 0],       # J/kg.K
             'Width': [0.3, 0.05, 0.013, 0, 0, 0],              # m
             'Slice': [1, 1, 1, 1, 1, 1]}                       # nb of meshes
materials = pd.DataFrame(
    materials, index=['Concrete' 'Insulation' 'Plaster' 'Glass' 'WoodDoor',
                      'WoodFloor'])

# Surfaces
surfaces = array
surfaces = {'LR': [13.11, 18.4, 6.6, 1.89, 48],      # m²
            'BR': [15, 3.8, 1.2, 0, 16],
            'LR-BR': [8.11, 0, 0, 1.89, 0]}
surfaces = pd.DataFrame(
    surfaces, index=['Dividingwall' 'Wall' 'Window' 'Door' 'Floor'])

# Radiative properties
# --------------------
σ = 5.67e-8     # W/m².K⁴ Stefan-Bolzmann constant

Fpw = 8.13 / 93.07     # view factor plaster - window (facteur de forme)
# RECALCULER AVEC SURFACE FIONA

Tm = 20 + 273   # mean temperature for radiative exchange

# convection coefficients, W/m² K
h = pd.DataFrame([{'in': 4., 'out': 10}])   # Valeurs À VÉRIFIER sur DB


# Thermal circuit (EN COURS DE MODIF)
# ===============

# Thermal conductances
# --------------------
# Conduction
# Conduction zone 1 : LR
Gcd_LR_c = materials['Conductivity'][0] / \
    materials['Width'][0] * surfaces['LR'][1]

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
# à insérer depuis github

# Capacity matrix C
# -----------------
# à insérer depuis github

# Vectors of temperature sources b
# --------------------------------
T0 = X      # outdoor temperature
T1 = X      # next room temperature
T2 = X      # temperature wanted in the livingroom
T3 = X      # temperature wanted in the bathroom

b = np.zeros(60)
b[[0, 12, 24, 45, 57, 59]] = T0
b[[8, 16, 49]] = T1
b[25] = T2
b[58] = T3

# Vectors of heat sources f
# -------------------------
