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

Sw_b = 1.23     # m² surface window in bathroom
Sw_l = 6.9      # m² surface window in livingroom
Sd = 2.2        # m² surface/door (2 doors in model)

Sc = 21.87      # m² surface concret
Si = 57.47      # m² surface insulation
Sp = 93.07      # m² surface plaster

# exemple : Sg = l**2     Sc = Si = 5 * Sg

# Air-flow rate
# -------------
Va = l * L * H      # m³ volume of air  #est-ce qu'on enlève les volumes mur?
ACH = 1             # air changes per hour
Va_dot = ACH * Va / 3600    # m³/s air infiltration

# Thermophyscal properties
# ------------------------
air = {'Density': 1.2,                      # kg/m³
       'Specific heat': 1000}               # J/kg.K

"""From DesignBuilder"""
dividingwall = {'Conductivity': [0.25, 0.0457, 0.25],      # W/m.K
                'Density': [28000, 40, 28000],             # kg/m³
                'Specific heat': [896, 1450, 896],         # J/kg.K
                'Width': [0.013, 0.05, 0.013],             # m
                'Surface': [XX, XX, XX],  # À COMPLÉTER    # m²
                'Slice': [1, 1, 1]}                        # nb of meshes
dividingwall = pd.DataFrame(
    dividingwall, index=['Plaster' 'Insulation' 'Plaster'])

wall = {'Conductivity': [2.3, 0.0457, 0.25],         # W/m.K
        'Density': [2300, 40, 28000],             # kg/m³
        'Specific heat': [1000, 1450, 896],       # J/kg.K
        'Width': [0.3, 0.05, 0.013],              # m
        'Surface': [XX, XX, XX],  # À COMPLÉTER   # m²
        'Slice': [1, 1, 1]}                       # nb of meshes
wall = pd.DataFrame(wall, index=['Concrete' 'Insulation' 'Plaster'])

# À COMPLÉTER depuis DesignBuilder
opening = {'Conductivity': [X, X],      # W/m.K
           'Density': [X, X],           # kg/m³
           'Specific heat': [X, X],     # J/kg.K
           'Width': [X, X],             # m
           'Surface': [XX, XX],         # m²
           'Slice': [1, 1]}             # nb of meshes
opening = pd.DataFrame(opening, index=['Window' 'Door'])

# Radiative properties
# --------------------
""" from DesignBuilder"""  # Valeurs à RÉCUPÉRER de DB
ε_cLW = 0.9     # long wave concrete emmisivity
α_cSW = 0.6     # short wave concrete absorptivity

ε_pLW = XX      # long wave plaster emmisivity
α_pSW = XX      # short wave plaster absorptivity

ε_wLW = XX     # long wave window emmisivity
α_wSW = XX     # short wave window absorptivity
τ_gSW = XX     # short wave window transmitance


σ = 5.67e-8     # W/m².K⁴ Stefan-Bolzmann constant

Fpw = 8.13 / 93.07     # view factor plaster - window (facteur de forme)
# VÉRIFIER LE CALCUL

Tm = 20 + 273   # mean temperature for radiative exchange

# convection coefficients, W/m² K
h = pd.DataFrame([{'in': 4., 'out': 10}])   # Valeurs À VÉRIFIER sur DB


# Thermal circuit (EN COURS DE MODIF)
# ===============

# Thermal conductances
# Conduction
Gd_cd = dividingwall['Conductivity'] / \
    dividingwall['Width'] * dividingwall['Surface']
Gw_cd = wall['Conductivity'] / wall['Width'] * wall['Surface']

# Convection
Gc_cv = h *
Gw_cv = h * wall['Surface'][0]     # wall
Gg_cv = h * wall['Surface'][2]     # glass
