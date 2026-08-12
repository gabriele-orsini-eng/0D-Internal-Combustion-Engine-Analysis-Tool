#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 09:06:49 2026

@author: gabriele
"""

#%% # =====================================================================
    # 1.2.1 IMPORT
    # =====================================================================

import numpy as np
from modules.InputData import BaseEngineData
from dataclasses import dataclass

#%% # =====================================================================
    # 1.2.2 DATACLASS OUTPUT
    # =====================================================================

@dataclass
class PreliminaryCalculation_Results:
    unit_displacement_cm3: float
    mean_piston_speed_ms: float
    stroke_to_bore_ratio: float
    lambda_crank_mm: float
    phi_max: float
    height_engine_structure_mm: float
    rho_Int: float
    sound_speed_ms: float
    intakevalve_area_total_mm2: float
    intakevalve_diameter_mm: float
    exhaustvalve_diameter_mm: float
    
#%% # =====================================================================
    # 1.2.3 CALCULATIONS
    # =====================================================================

"""
This function calculate additional generic data for the sub-sequent engine calculations such as mean piston speed, air condition in the intake 
environment and intake/exhaust valve diameter based on the index approach
"""

def Preliminary_Calculation(EngineData: BaseEngineData):
    
    # Cylinder unit displacement calculation [cm3]
    unit_displacement_cm3 = ((np.pi/4)*np.power(EngineData.piston_bore_mm, 2)*EngineData.piston_stroke_mm)/1000 
    
    # Cngine mean speed [m/s]
    mean_piston_speed_ms = (2*EngineData.max_engine_speed_rpm*EngineData.piston_stroke_mm)/(60*1000) 
    
    stroke_to_bore_ratio = EngineData.piston_stroke_mm/EngineData.piston_bore_mm
    lambda_crank_mm = EngineData.crank_radius_mm/EngineData.connecting_rod_length_mm
    
    phi_max = np.degrees(np.asin(lambda_crank_mm))
    
    # Engine block total height w/o head [mm]
    height_engine_structure_mm = (EngineData.connecting_rod_length_mm + 
                                  EngineData.piston_compression_height_mm + 
                                  EngineData.crank_radius_mm)
    
    
    rho_Int = 349*EngineData.intake_pressure_bar/(EngineData.intake_temperature_deg+273.15)
    sound_speed_ms = EngineData.temperature_coefficient_sound*np.sqrt((EngineData.intake_temperature_deg+273.15))
    
    # Intake valve total area [mm3]
    intakevalve_area_total_mm2 = (((EngineData.piston_area/np.pow(10, 6))*mean_piston_speed_ms)/(EngineData.intakevalve_discharge_coefficient*sound_speed_ms*EngineData.mach_coefficient))*np.pow(10, 6)
    
    # Single intake & exhaust valve diameter
    intakevalve_diameter_mm = np.sqrt(intakevalve_area_total_mm2*EngineData.number_intake_valves/np.pi)
    exhaustvalve_diameter_mm = intakevalve_diameter_mm*0.7
    
    return PreliminaryCalculation_Results(
        unit_displacement_cm3 = unit_displacement_cm3,
        mean_piston_speed_ms = mean_piston_speed_ms,
        stroke_to_bore_ratio = stroke_to_bore_ratio,
        lambda_crank_mm = lambda_crank_mm,
        phi_max = phi_max,
        height_engine_structure_mm = height_engine_structure_mm,
        rho_Int = rho_Int,
        sound_speed_ms = sound_speed_ms,
        intakevalve_area_total_mm2 = intakevalve_area_total_mm2,
        intakevalve_diameter_mm = intakevalve_diameter_mm,
        exhaustvalve_diameter_mm = exhaustvalve_diameter_mm)
