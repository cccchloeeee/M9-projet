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
h = 2.5             # m hauteur du studio

Sw_b = 1.23     # m² surface window in bathroom
Sw_l = 6.9      # m² surface window in livingroom
Sd = 2.2        # m² surface/door (2 doors in model)

Sc = 21.87      # m² surface concret
Si = 57.47      # m² surface insulation
Sp = 93.07      # m² surface plaster

# exemple : Sg = l**2     Sc = Si = 5 * Sg

# Air-flow rate
# -------------
Va = l*L*h          # m³ volume of air  #est-ce qu'on enlève les volumes mur?
ACH = 1             # air changes per hour
Va_dot = ACH * Va / 3600    # m³/s air infiltration

# Thermophyscal properties
# ------------------------
air = {'Density': 1.2,                      # kg/m³
       'Specific heat': 1000}               # J/kg.K

"""From DesignBuilder"""
cloison = {'Conductivity': [0.25, 0.0457, 0.25],      # W/m.K
           'Density': [28000, 40, 28000],             # kg/m³
           'Specific heat': [896, 1450, 896],         # J/kg.K
           'Width': [0.013, 0.05, 0.013],             # m
           'Surface': [XX, XX, XX],  # À COMPLÉTER    # m²
           'Slice': [1, 1, 1]}                        # nb of meshes
cloison = pd.DataFrame(cloison, index=['Plaster' 'Insulation' 'Plaster'])

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
""" from DesignBuilder"""
ε_cLW = 0.9     # long wave concrete emmisivity
α_cSW = 0.6     # short wave concrete absorptivity

ε_pLW = XX      # long wave plaster emmisivity
α_pSW = XX      # short wave plaster absorptivity

ε_wLW = XX     # long wave window emmisivity
α_wSW = XX     # short wave window absorptivity
τ_gSW = XX     # short wave window transmitance


# exemple tuto03 de ghiauss (À VÉRIFIER ou alors on prend depuis DB)
""" concrete EngToolbox Emissivity Coefficient Materials """
ε_wLW = 0.9     # long wave wall emmisivity
""" grey to dark surface EngToolbox,
    Absorbed Solar Radiation by Surface Color """
α_wSW = 0.2     # absortivity white surface

""" Glass, pyrex EngToolbox Absorbed Solar Radiation bySurface Color """
ε_gLW = 0.9     # long wave glass emmisivity

""" EngToolbox Optical properties of some typical glazing mat
    Window glass """
τ_gSW = 0.83    # short wave glass transmitance

α_gSW = 0.1     # short wave glass absortivity


σ = 5.67e-8     # W/m².K⁴ Stefan-Bolzmann constant

Fwg = 8.13 / 93.07     # view factor plaster - window (facteur de forme)

Tm = 20 + 273   # mean temperature for radiative exchange

# convection coefficients, W/m² K
h = pd.DataFrame([{'in': 4., 'out': 10}])   # Valeurs À VÉRIFIER sur DB


# Thermal circuit (À MODIFIER, C'EST ENCORE LES LIGNES DE GHIAUSS)
# ===============

# Thermal conductances
# Conduction
Gc_cd = cloison['Conductivity'] / cloison['Width'] * cloison['Surface']
Gw_cd = wall['Conductivity'] / wall['Width'] * wall['Surface']

# Convection
Gc_cv = h *
Gw_cv = h * wall['Surface'][0]     # wall
Gg_cv = h * wall['Surface'][2]     # glass

# Long-wave radiation exchnage
GLW1 = ε_wLW / (1 - ε_wLW) * wall['Surface']['Insulation'] * 4 * σ * Tm**3
GLW2 = Fwg * wall['Surface']['Insulation'] * 4 * σ * Tm**3
GLW3 = ε_gLW / (1 - ε_gLW) * wall['Surface']['Glass'] * 4 * σ * Tm**3
# long-wave exg. wall-glass
GLW = 1 / (1 / GLW1 + 1 / GLW2 + 1 / GLW3)

# ventilation & advection
Gv = Va_dot * air['Density'] * air['Specific heat']

# glass: convection outdoor & conduction
Ggs = float(1 / (1 / Gg['out'] + 1 / (2 * G_cd['Glass'])))
