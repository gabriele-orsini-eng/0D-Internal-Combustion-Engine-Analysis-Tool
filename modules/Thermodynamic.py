#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:00:49 2026

@author: gabriele
"""

#%% # =====================================================================
    # 1.3.1 IMPORT
    # =====================================================================

import numpy as np
from modules.InputData import BaseEngineData
from modules.InputData import ThermodynamicData
from modules.PreliminaryCalculation import PreliminaryCalculation_Results
from dataclasses import dataclass

#%% # =====================================================================
    # 1.3.2 DATACLASS OUTPUT
    # =====================================================================

@dataclass
class ThermodynamicCalculation_Results:
    V_chamber_cm3: float
    M_Air_Th_g: float
    M_Air_Re_g: float
    M_Comb_g: float
    Q_In_J: float
    P_In_kwatt: float
    P_Eff_estimated_cv: float
    fuel_burn_fraction_10deg: float
    piston_postion_mm: float
    piston_speed_ms: float
    piston_acceleration: float
    V_chamber_inst_cm3: float
    DVChamber_Dteta: float
    Df_DTeta: float
    Wiebe_fraction: float
    P_Wiebe_bar: float
    Dq_DTeta: float
    Angle_Degree: float

#%% # =====================================================================
    # 1.3.3 CALCULATIONS
    # =====================================================================

"""
This function calculate quantities relative to the cranktrain kinematics such as motion and about
it's dynamic like the gas force
"""

def Thermodynamic_Calculation(EngineData: BaseEngineData, ThermData: ThermodynamicData, PreCalc: PreliminaryCalculation_Results):

    # engine combustion chamber volume [cm3]
    V_chamber_cm3 = PreCalc.unit_displacement_cm3/(ThermData.compression_ratio-1)
    
    # Cylinder therical and real air mass [g]
    M_Air_Th_g = (PreCalc.unit_displacement_cm3*PreCalc.rho_Int)/1000
    M_Air_Re_g = M_Air_Th_g*ThermData.lambda_engine
    
    # Heat into cylinder [J]
    M_Comb_g = M_Air_Re_g/ThermData.fuel_metering
    Q_In_J = M_Comb_g*ThermData.low_heating_value
    
    # Engine power [KW]
    P_In_kwatt = Q_In_J/(EngineData.piston_stroke_mm/PreCalc.mean_piston_speed_ms)
    P_Eff_estimated_cv = (((PreCalc.rho_Int/1000)*EngineData.cylinders_number*ThermData.lambda_engine*
                           PreCalc.unit_displacement_cm3*(EngineData.max_engine_speed_rpm/120)*
                           (ThermData.low_heating_value/ThermData.fuel_metering)*
                           ThermData.engine_total_efficiency)*0.00136)
    
    # Fuel burn fraction 10° after PMS
    fuel_burn_fraction_10deg = (1-np.exp(-ThermData.wiebe_efficiency_factor*
                                        np.pow((np.radians(10)-np.radians(ThermData.start_combustion_angle_deg))
                                        /(np.radians(ThermData.end_combustion_angle_deg)-
                                        np.radians(ThermData.start_combustion_angle_deg)), ThermData.wiebe_shape_factor)))
    
    # Vector with angle value for next calculations
    Angle_Degree = np.linspace(0, 720, 721)
    Angle_Radians = np.radians(Angle_Degree)
    
    # Piston position [mm]
    piston_postion_mm = (EngineData.crank_radius_mm*(1-np.cos(Angle_Radians)+(1/PreCalc.lambda_crank_mm)*
                        (1-(np.power((1-np.power(PreCalc.lambda_crank_mm*np.sin(Angle_Radians),2)),0.5)))))                                                    
    
    # Crankshaft speed in [rad/s]
    omega_max = (2*np.pi/60)*EngineData.max_engine_speed_rpm
    
    # Piston speed [m/s]
    piston_speed_ms = (omega_max*(EngineData.crank_radius_mm/1000)*(np.sin(Angle_Radians)+
                      (PreCalc.lambda_crank_mm/2)*np.sin(2*Angle_Radians)))
    
    # Piston acceleration [m/s2]
    piston_acceleration = (np.power(omega_max, 2)*(EngineData.crank_radius_mm/1000)*
                          (np.cos(Angle_Radians)+PreCalc.lambda_crank_mm*np.cos(2*Angle_Radians)))
    
    # Combustion chamber instantanueos volume [cm3]
    V_chamber_inst_cm3 = ((((np.pi/4)*(np.power(EngineData.piston_bore_mm, 2))*piston_postion_mm)/1000)+
                         V_chamber_cm3)
    
    # Rate of change combustion chamber as a function of crank angle [cm3/rad]
    DVChamber_Dteta = (np.pi/4)*np.power((EngineData.piston_bore_mm/10), 2)*(piston_speed_ms*100)/omega_max
    
    # Wiebe function calculation
    Angle_Start = 360+ThermData.start_combustion_angle_deg
    Angle_In = Angle_Degree[Angle_Degree < Angle_Start]
    Angle_End = Angle_Degree[Angle_Degree >= Angle_Start]
    
    # Initialize Wiebe burn fraction, it goes from 0 to 1
    Wiebe_In = np.zeros(len(Angle_In))
    
    Delta_Teta_Rad = np.radians(ThermData.end_combustion_angle_deg-ThermData.start_combustion_angle_deg)
    Angle_Ratio = np.radians((Angle_End-(360 + ThermData.start_combustion_angle_deg)))/Delta_Teta_Rad
    
    Wiebe_End = (1 - np.exp(-ThermData.wiebe_efficiency_factor*
                np.power(Angle_Ratio, ThermData.wiebe_shape_factor)))
    
    Wiebe_fraction = np.concatenate((Wiebe_In, Wiebe_End))
    
    # Burn fraction as a function of the crank angle [-/rad]
    Df_DTeta_In = np.zeros(len(Angle_In))
    
    Df_DTeta_End = ((1-Wiebe_End)*ThermData.wiebe_shape_factor*ThermData.wiebe_efficiency_factor/
                    Delta_Teta_Rad*np.power(Angle_Ratio, (ThermData.wiebe_shape_factor -1)))
    
    Df_DTeta = np.concatenate((Df_DTeta_In,Df_DTeta_End))
    
    # Energy as a function of the crank angle [J/rad]
    Dq_DTeta = Q_In_J*Df_DTeta*ThermData.engine_adiabatic_efficiency*ThermData.engine_combustion_efficiency
    
    Angle_End = 360+ThermData.end_combustion_angle_deg
    
    # Compute Wiebe pressure [bar]
    P_Wiebe_bar = np.zeros(len(Angle_Degree))
    Dp_DTeta = np.zeros(len(Angle_Degree))
    P_Wiebe_bar[0] = EngineData.intake_pressure_bar
    
    for i in range(1, len(Angle_Degree)):
        Angle = Angle_Degree[i]
        P_Wiebe_pr = P_Wiebe_bar[i-1]
        Vol_Mod = V_chamber_inst_cm3[i-1]/V_chamber_inst_cm3[i]
        Rad_Mod = np.radians(Angle_Degree[i]-Angle_Degree[i-1])
        if Angle <= 180:
            P_Wiebe_bar[i] = EngineData.intake_pressure_bar
        elif Angle < (Angle_Start):
            P_Wiebe_bar[i] = P_Wiebe_pr*Vol_Mod**ThermData.polytropic_coeff_compression
        elif (Angle >= Angle_Start) & (Angle <= Angle_End):
            K = Dq_DTeta[i]
            Dp_DTeta_Scalar = (
                ((ThermData.polytropic_coeff_combustion-1)/
                V_chamber_inst_cm3[i]*K*10)-(ThermData.polytropic_coeff_combustion*
                P_Wiebe_pr/V_chamber_inst_cm3[i]*DVChamber_Dteta[i])
                               )
            Dp_DTeta[i] = Dp_DTeta_Scalar
            P_Wiebe_bar[i] = Dp_DTeta_Scalar*Rad_Mod+P_Wiebe_pr
        elif Angle < 540:
            P_Wiebe_bar[i] = P_Wiebe_pr*Vol_Mod**ThermData.polytropic_coeff_expansion
        else:
            P_Wiebe_bar[i] = ThermData.exhaust_pressure_bar
            
    return ThermodynamicCalculation_Results(
        V_chamber_cm3 = V_chamber_cm3,
        M_Air_Th_g = M_Air_Th_g,
        M_Air_Re_g = M_Air_Re_g,
        M_Comb_g = M_Comb_g,
        Q_In_J = Q_In_J,
        P_In_kwatt = P_In_kwatt,
        P_Eff_estimated_cv = P_Eff_estimated_cv,
        fuel_burn_fraction_10deg = fuel_burn_fraction_10deg,
        piston_postion_mm = piston_postion_mm,
        piston_speed_ms = piston_speed_ms,
        piston_acceleration = piston_acceleration,
        V_chamber_inst_cm3 = V_chamber_inst_cm3,
        DVChamber_Dteta = DVChamber_Dteta,
        Df_DTeta = Df_DTeta,
        Wiebe_fraction = Wiebe_fraction,
        P_Wiebe_bar = P_Wiebe_bar,
        Dq_DTeta = Dq_DTeta,
        Angle_Degree = Angle_Degree
        )
