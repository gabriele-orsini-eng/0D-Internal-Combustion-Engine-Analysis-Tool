#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:52:59 2026

@author: gabriele
"""

from pathlib import Path 
import matplotlib.pyplot as plt
import numpy as np
from modules.Thermodynamic import ThermodynamicCalculation_Results
from modules.Pressure_scaling import PressureScaling_Results
from modules.Engine_force import EngineForce_Results

BASE_DIR = Path(__file__).resolve().parent

style_path = BASE_DIR / "Engine_Style.mplstyle"

plt.style.use(str(style_path))

def cylinder_pressure(ThermDataResults: ThermodynamicCalculation_Results):
    fig_Cyl_Pressure = plt.figure(figsize=(9, 5.5), dpi=300)
    plt.plot(ThermDataResults.Angle_Degree, ThermDataResults.P_Wiebe_bar)
    plt.title("In-Cylinder Pressure")
    plt.xlabel("Crank Angle [°]")
    plt.ylabel("Pressure [bar]")
    plt.xticks([0, 180, 360, 540, 720])
    plt.xlim(0, 720)
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, np.round(np.max(ThermDataResults.P_Wiebe_bar)+20)])
    plt.ylim(0, np.round(np.max(ThermDataResults.P_Wiebe_bar)+20))
    plt.gca().minorticks_on()
    plt.axvline(x=180, color='#4393c3', linestyle=':', linewidth=1.5, label='BDC Intake')
    plt.axvline(x=360, color='#d95f02', linestyle=':', linewidth=1.5, label='TDC')
    plt.axvline(x=540, color='#7570b3', linestyle=':', linewidth=1.2, label='BDC Exhaust')
    plt.grid(True)    
    plt.tight_layout()
    return fig_Cyl_Pressure
    
def indicating_diagram(ThermDataResults: ThermodynamicCalculation_Results):
    import numpy as np
    P_pa = ThermDataResults.P_Wiebe_bar * 1e5
    V_m3 = ThermDataResults.V_chamber_inst_cm3 * 1e-6
    indicated_work = np.abs(np.trapezoid(P_pa, V_m3))
    fig_indicating_diagram = plt.figure(figsize=(9, 5.5), dpi=100)
    plt.fill(ThermDataResults.V_chamber_inst_cm3, ThermDataResults.P_Wiebe_bar, alpha=0.15, label='Indicated Work')
    plt.plot(ThermDataResults.V_chamber_inst_cm3, ThermDataResults.P_Wiebe_bar)
    plt.annotate(
        f'Indicated Work:\n{indicated_work:.1f} J',
        xy=(45, 25),                    
        xytext=(90, 45),                
        arrowprops=dict(
            arrowstyle="->", 
            connectionstyle="arc3,rad=.15", 
            color="#333333", 
            lw=1.2
        ),
        bbox=dict(
            boxstyle="round,pad=0.5", 
            facecolor="#ffffff", 
            edgecolor="#cccccc", 
            alpha=0.9
        ),
        fontsize=10,
        fontweight='bold'
    )
    plt.title("P-V Diagram", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Volume [cm^3]", fontsize=11, labelpad=8)
    plt.ylabel("Pressure [bar]", fontsize=11, labelpad=8)
    plt.xticks([0, 30, 60, 90, 120, 150, 180])
    plt.xlim(0, 180)
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, np.round(np.max(ThermDataResults.P_Wiebe_bar)+20)])
    plt.ylim(0, np.round(np.max(ThermDataResults.P_Wiebe_bar)+20))
    plt.gca().minorticks_on()
    plt.grid(True, which='both', color='#e2e2e2', linestyle='--', linewidth=0.7)    
    plt.tight_layout()
    return fig_indicating_diagram

    

def pressure_scaled(ThermDataResults: ThermodynamicCalculation_Results, PS_Results: PressureScaling_Results):
    fig_PScaled = plt.figure(figsize=(9, 5.5), dpi=100)
    plt.plot(ThermDataResults.Angle_Degree, PS_Results.P_Motored_bar, label = "Pressure Motored")
    plt.plot(ThermDataResults.Angle_Degree, ThermDataResults.P_Wiebe_bar, label = "Original Pressure Curve")
    plt.plot(ThermDataResults.Angle_Degree, PS_Results.P_New_bar, label = "Pressue Curve at new PFP")
    plt.title("In-Cylinder Pressure", fontsize=14, fontweight='bold', pad=15)
    plt.legend(loc='best', edgecolor='#cccccc', shadow=False)
    plt.xlabel("Crank Angle [°]", fontsize=11, labelpad=8)
    plt.ylabel("Pressure [bar]", fontsize=11, labelpad=8)
    plt.xticks([0, 180, 360, 540, 720])
    plt.xlim(0, 720)
    plt.ylim(0, np.round(np.max(PS_Results.P_New_bar)+20))
    plt.gca().minorticks_on()
    plt.axvline(x=180, color='#4393c3', linestyle=':', linewidth=1.5, label='BDC Intake')
    plt.axvline(x=360, color='#d95f02', linestyle=':', linewidth=1.5, label='TDC')
    plt.axvline(x=540, color='#7570b3', linestyle=':', linewidth=1.2, label='BDC Exhaust')
    plt.grid(True, which='major', color='#d3d3d3', linestyle='--', linewidth=0.8)
    plt.grid(True, which='minor', color='#e8e8e8', linestyle=':', linewidth=0.5)
    plt.tight_layout()
    return fig_PScaled

def indicating_diagram_PFP(ThermDataResults: ThermodynamicCalculation_Results, PS_Results: PressureScaling_Results):
    import numpy as np
    P_pa = PS_Results.P_New_bar * 1e5
    V_m3 = ThermDataResults.V_chamber_inst_cm3 * 1e-6
    indicated_work = np.abs(np.trapezoid(P_pa, V_m3))
    fig_indicating_diagram_PFP = plt.figure(figsize=(9, 5.5), dpi=100)
    plt.fill(ThermDataResults.V_chamber_inst_cm3, PS_Results.P_New_bar, alpha=0.15, label='Indicated Work')
    plt.plot(ThermDataResults.V_chamber_inst_cm3, PS_Results.P_New_bar)
    plt.annotate(
        f'Indicated Work:\n{indicated_work:.1f} J',
        xy=(45, 25),                    
        xytext=(90, 45),                
        arrowprops=dict(
            arrowstyle="->", 
            connectionstyle="arc3,rad=.15", 
            color="#333333", 
            lw=1.2
        ),
        bbox=dict(
            boxstyle="round,pad=0.5", 
            facecolor="#ffffff", 
            edgecolor="#cccccc", 
            alpha=0.9
        ),
        fontsize=10,
        fontweight='bold'
    )
    plt.title("P-V Diagram", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Volume [cm^3]", fontsize=11, labelpad=8)
    plt.ylabel("Pressure [bar]", fontsize=11, labelpad=8)
    plt.xticks([0, 30, 60, 90, 120, 150, 180])
    plt.xlim(0, 180)
    plt.ylim(0, np.round(np.max(PS_Results.P_New_bar)+20))
    plt.gca().minorticks_on()
    plt.grid(True, which='both', color='#e2e2e2', linestyle='--', linewidth=0.7)    
    plt.tight_layout()
    return fig_indicating_diagram_PFP
    
def Eng_forces(ThermDataResults: ThermodynamicCalculation_Results, EngForce: EngineForce_Results):
    fig_EngForces = plt.figure(figsize=(9, 5.5), dpi=100)
    plt.plot(ThermDataResults.Angle_Degree, EngForce.F_tot, label='Total Force')
    plt.plot(ThermDataResults.Angle_Degree, EngForce.FLat, label='Lateral Force')
    plt.title("Cranktrain Engine Forces", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Crank Angle [°]", fontsize=11, labelpad=8)
    plt.ylabel("[N]", fontsize=11, labelpad=8)
    plt.xticks([0, 180, 360, 540, 720])
    plt.xlim(0, 720)
    plt.yticks([-30000, -25000, -20000, -15000, -10000, -5000, 0, 5000, 10000, 15000])
    plt.ylim(-30000, 15000)
    plt.gca().minorticks_on()
    plt.axvline(x=180, color='#4393c3', linestyle=':', linewidth=1.5, label='BDC Intake')
    plt.axvline(x=360, color='#d95f02', linestyle=':', linewidth=1.5, label='TDC')
    plt.axvline(x=540, color='#7570b3', linestyle=':', linewidth=1.2, label='BDC Exhaust')
    plt.grid(True, which='both', color='#e2e2e2', linestyle='--', linewidth=0.7)  
    plt.legend(loc='best', edgecolor='#cccccc', shadow=False)
    plt.tight_layout()
    return fig_EngForces
    
def Eng_torques(ThermDataResults: ThermodynamicCalculation_Results, EngForce: EngineForce_Results):
    fig_EngTorques = plt.figure(figsize=(9, 5.5), dpi=100)
    plt.plot(ThermDataResults.Angle_Degree, EngForce.torque_ist_nm, label='Istantaneos Torque')
    plt.title("Cranktrain Engine Torque", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Crank Angle [°]", fontsize=11, labelpad=8)
    plt.ylabel("[Nm]", fontsize=11, labelpad=8)
    plt.xticks([0, 180, 360, 540, 720])
    plt.xlim(0, 720)
    plt.yticks([-200, -150, -100, -50, 0, 50, 100, 150, 200])
    plt.ylim(-200, 200)
    plt.gca().minorticks_on()
    plt.axvline(x=180, color='#4393c3', linestyle=':', linewidth=1.5, label='BDC Intake')
    plt.axvline(x=360, color='#d95f02', linestyle=':', linewidth=1.5, label='TDC')
    plt.axvline(x=540, color='#7570b3', linestyle=':', linewidth=1.2, label='BDC Exhaust')
    plt.grid(True, which='both', color='#e2e2e2', linestyle='--', linewidth=0.7)  
    plt.legend(loc='best', edgecolor='#cccccc', shadow=False)
    plt.tight_layout()
    return fig_EngTorques


