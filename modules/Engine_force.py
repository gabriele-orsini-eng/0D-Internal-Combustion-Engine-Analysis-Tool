#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:32:11 2026

@author: gabriele
"""

#%% # =====================================================================
    # 1.7.1 IMPORT
    # =====================================================================
    
import numpy as np
from modules.InputData import BaseEngineData
from modules.InputData import Cranktrain_Masses
from modules.InputData import ThermodynamicData
from modules.PreliminaryCalculation import PreliminaryCalculation_Results
from modules.Thermodynamic import ThermodynamicCalculation_Results
from dataclasses import dataclass

#%% # =====================================================================
    # 1.7.2 DATACLASS OUTPUT
    # =====================================================================

@dataclass
class EngineForce_Results:
    Fa: float
    Fg: float
    F_tot: float
    FLat: float
    Fb: float
    Tg: float
    Tin: float
    T_tot: float
    R_1: float
    R_2: float
    torque_ist_nm: float
    torque_avg_nm: float
    piston_alt_mass_g: float
    conrod_alt_mass_g: float
    conrod_rot_mass_g: float
    

#%% # =====================================================================
    # 1.7.3 CALCULATIONS
    # =====================================================================

    """
    This function calculate the forces that apply to the cranktrain
    """
    
def Engine_force(EngineData: BaseEngineData, CrankMass: Cranktrain_Masses,
                 ThermDataResults: ThermodynamicCalculation_Results,
                 ThermData: ThermodynamicData, PreCalc: PreliminaryCalculation_Results):
    # Additional Mass data [g]
    seg_tot_mass_g = CrankMass.seg_1_mass_g + CrankMass.seg_2_mass_g + CrankMass.seg_oil_mass_g
    m_b_tot_mass_g =CrankMass.conrod_assembly_mass_g + CrankMass.bushing_mass_g
    
    g_b_tot_mm = (CrankMass.conrod_assembly_mass_g*CrankMass.cog_conrod_mm)/m_b_tot_mass_g
    conrod_alt_mass_g = (m_b_tot_mass_g*g_b_tot_mm)/EngineData.connecting_rod_length_mm
    conrod_rot_mass_g = (m_b_tot_mass_g*(EngineData.connecting_rod_length_mm-g_b_tot_mm))/EngineData.connecting_rod_length_mm
    piston_alt_mass_g = CrankMass.piston_mass_g + seg_tot_mass_g + CrankMass.piston_pin_mass_g + (2*CrankMass.pin_ring_mass_g)
    alt_mass_tot_g = piston_alt_mass_g + conrod_alt_mass_g
    
    # Inertia Force [N]
    Fa = (alt_mass_tot_g*ThermDataResults.piston_acceleration)/1000
    
    # Gas Force [N]
    Fg = ((ThermData.counter_pressure_carter_bar-ThermDataResults.P_Wiebe_bar)
          *(np.pi/4)*((EngineData.piston_bore_mm/1000)**2)*(10**5))
    
    #Total Force [N]
    
    F_tot = Fa + Fg
    
    phi_degree = np.arcsin(PreCalc.lambda_crank_mm*np.sin(np.radians(ThermDataResults.Angle_Degree)))*(180/np.pi)
    phi_rad = np.radians(phi_degree)
    
    # Lateral Force [N]
    FLat = F_tot*np.tan(phi_degree*(np.pi/180))
    Fb = F_tot/np.cos(phi_rad)
    
    # Gas Tangential Force [N]
    Tg = -Fg*np.sin(np.radians(ThermDataResults.Angle_Degree+phi_degree))/np.cos(phi_rad)
    
    # Inertial Tangential Force [N]
    Tin = -Fa*np.sin(np.radians(ThermDataResults.Angle_Degree+phi_degree))/np.cos(phi_rad)
    T_tot = Tg + Tin 
    
    
    R_1 = -Fb*np.cos(np.radians(ThermDataResults.Angle_Degree+phi_degree))
    R_2 = -1*(EngineData.max_engine_speed_rpm*2*np.pi/60)**2*(EngineData.crank_radius_mm/1000)*( conrod_rot_mass_g+CrankMass.conrod_pin_mass_g)/1000
    
    L = np.zeros(len(ThermDataResults.V_chamber_inst_cm3))
    
    for i in range (1, len(ThermDataResults.V_chamber_inst_cm3)):
        Vol_Diff = ThermDataResults.V_chamber_inst_cm3[i]-ThermDataResults.V_chamber_inst_cm3[i-1]
        P_Wiebe_Sum = ThermDataResults.P_Wiebe_bar[i]+ThermDataResults.P_Wiebe_bar[i-1]
        L[i] = Vol_Diff*(P_Wiebe_Sum/2)
    
    L = np.sum(L)/10
    
    torque_ist_nm = T_tot*EngineData.crank_radius_mm/1000
    
    torque_avg_nm = np.zeros(len(ThermDataResults.Angle_Degree))
    
    for i in range (1, len(ThermDataResults.Angle_Degree)):
        Angle_Diff = ThermDataResults.Angle_Degree[i]-ThermDataResults.Angle_Degree[i-1]
        M_Sum = torque_ist_nm[i]+torque_ist_nm[i-1]
        torque_ist_nm[i] = Angle_Diff*(M_Sum/2)
    
    torque_avg_nm = np.sum(torque_ist_nm)/720
    
    return EngineForce_Results(
        Fa = Fa,
        Fg = Fg,
        F_tot = F_tot,
        FLat = FLat,
        Fb = Fb,
        Tg = Tg,
        Tin = Tin,
        T_tot = T_tot,
        R_1 = R_1,
        R_2 = R_2,
        torque_ist_nm = torque_ist_nm,
        torque_avg_nm = torque_avg_nm,
        piston_alt_mass_g =  piston_alt_mass_g,
        conrod_alt_mass_g =  conrod_alt_mass_g,
        conrod_rot_mass_g =  conrod_rot_mass_g
        )
    

