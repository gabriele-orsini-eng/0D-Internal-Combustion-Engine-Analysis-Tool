#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:18:30 2026

@author: gabriele
"""

#%% # =====================================================================
    # 1.4.1 IMPORT
    # =====================================================================
    
import numpy as np
from dataclasses import dataclass
from modules.InputData import BaseEngineData
from modules.InputData import ThermodynamicData
from modules.Thermodynamic import ThermodynamicCalculation_Results

#%% # =====================================================================
    # 1.4.2 DATACLASS OUTPUT
    # =====================================================================
    
@dataclass
class PressureScaling_Results:
    PFP_Base: float
    Scale: float
    P_New_bar: float
    P_Motored_bar: float

#%% # =====================================================================
    # 1.4.3 CALCULATIONS
    # =====================================================================

'''
This function allows the pressure scaling to a new PFP target by decomposing the signal into two parts. One
for the motored one and one for the combustion
'''

def Pressure_scaling(EngineData: BaseEngineData, ThermData: ThermodynamicData, ThermDataResults: ThermodynamicCalculation_Results):
    
    
    idx_180 = np.abs(ThermDataResults.Angle_Degree - 180).argmin()
    Vol_IVC = ThermDataResults.V_chamber_inst_cm3[idx_180]
    
    P_Motored_bar = np.zeros(len(ThermDataResults.Angle_Degree))
    
    cond_int = ThermDataResults.Angle_Degree <= 180
    cond_comp_exp = (ThermDataResults.Angle_Degree > 180) & (ThermDataResults.Angle_Degree < 540)
    cond_exh = ThermDataResults.Angle_Degree >= 540
    
    
    P_Motored_bar[cond_int] = EngineData.intake_pressure_bar
    P_Motored_bar[cond_comp_exp] = (EngineData.intake_pressure_bar * 
                                (Vol_IVC / ThermDataResults.V_chamber_inst_cm3[cond_comp_exp]) **
                                ThermData.polytropic_coeff_compression)
    
    P_Motored_bar[cond_exh] = ThermData.exhaust_pressure_bar
    
    
    P_Combustion_bar = ThermDataResults.P_Wiebe_bar - P_Motored_bar
    P_Combustion_bar = np.maximum(0, P_Combustion_bar)
    
    PFP_Base = np.max(ThermDataResults.P_Wiebe_bar)
    Index_PFP_Base = np.argmax(ThermDataResults.P_Wiebe_bar)
    PFP_Target = ThermData.pfp
    
    
    P_Motored_at_PFP = P_Motored_bar[Index_PFP_Base]
    Scale = (PFP_Target - P_Motored_at_PFP) / (PFP_Base - P_Motored_at_PFP)
    
    
    P_New_bar = P_Motored_bar + Scale * P_Combustion_bar
    
    return  PressureScaling_Results(
        PFP_Base = PFP_Base,
        Scale = Scale,
        P_New_bar = P_New_bar,
        P_Motored_bar = P_Motored_bar
        )