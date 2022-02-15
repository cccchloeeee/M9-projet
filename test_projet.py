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
h = 3.5             # m hauteur du studio

# À COMPLÉTER
Sw =                # m² surface window
Sc =                # m² surface concret
Si =                # m² surface insulation
Sp =                # m² surface plaster
Sd =                # m² surface door
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

# Radiative properties (À VÉRIFIER si on garde les mêmes ?)
# --------------------
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

# pour connaitre facteur de forme --> connaitre les surfaces
Fwg = 1 / X     # view factor wall - glass
Tm = 20 + 273   # mean temp for radiative exchange
