#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 22:08:10 2026

@author: gabriele
"""

#%% # =====================================================================
    # 1.0 IMPORT MODULES
    # =====================================================================

import os
from pathlib import Path 
import modules.InputData as InputData
import modules.PreliminaryCalculation as pc
import modules.Thermodynamic as therm
import modules.Pressure_scaling as psca
import modules.Engine_force as EnFr
import modules.Plot as plot
from report.Report import report_generation


def main():
    
    BASE_DIR = Path(__file__).resolve().parent
    
    data_file = BASE_DIR / "templates" / "EngineData.xlsx"

#%% # =====================================================================
    # 1.1 INPUT DATA
    # =====================================================================

    BaseEngineData = InputData.read_excel_BaseEngineData(data_file)

    ThermodynamicData = InputData.read_excel_Thermodynamic(data_file)
    
    Cranktrain_Masses = InputData.read_excel_cranktrain_masses(data_file)
    
#%% # =====================================================================
    # 1.2 PRELIMINARY CALCULATION
    # =====================================================================

    PreliminaryCalculation_Results = pc.Preliminary_Calculation(BaseEngineData)

#%% # =====================================================================
    # 1.3 KINEMATIC & THERMODYNAMIC CALCULATION
    # =====================================================================
 
    ThermodynamicCalculation_Results = therm.Thermodynamic_Calculation(BaseEngineData, ThermodynamicData, PreliminaryCalculation_Results)

#%% # =====================================================================
    # 1.4 PRESSURE SCALING
    # =====================================================================

    PressureScaling_Results = None
    if int(ThermodynamicData.pressure_scaling) == 1:
        PressureScaling_Results = psca.Pressure_scaling(BaseEngineData, ThermodynamicData, ThermodynamicCalculation_Results)

#%% # =====================================================================
    # 1.7 ENGINE FORCES
    # =====================================================================

    EngineForce_Results = EnFr.Engine_force(BaseEngineData, Cranktrain_Masses, ThermodynamicCalculation_Results,
                         ThermodynamicData, PreliminaryCalculation_Results)
    
#%% # =====================================================================
    # PLOTS & REPORTS
    # =====================================================================

    output_folder = BASE_DIR / "engine_plots_output"
    output_folder.mkdir(parents=True, exist_ok=True)

    fig_Cyl_Pressure = plot.cylinder_pressure(ThermDataResults = ThermodynamicCalculation_Results)

    nome_file = os.path.join(output_folder, "Wiebe Cylinder Pressure.png")
    
    fig_Cyl_Pressure.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    fig_indicating_diagram = plot.indicating_diagram(ThermDataResults = ThermodynamicCalculation_Results)
    
    nome_file = os.path.join(output_folder, "Indicating Diagram.png")
    
    fig_indicating_diagram.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    fig_PScaled = plot.pressure_scaled(ThermDataResults = ThermodynamicCalculation_Results, PS_Results = PressureScaling_Results)

    nome_file = os.path.join(output_folder, "Pressure Scaled to New PFP.png")
    
    fig_PScaled.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    fig_indicating_diagram_PFP = plot.indicating_diagram_PFP(ThermDataResults = ThermodynamicCalculation_Results, PS_Results = PressureScaling_Results)
    
    nome_file = os.path.join(output_folder, "Indicating Diagram at New PFP.png")
    
    fig_indicating_diagram_PFP.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    fig_EngForces = plot.Eng_forces(ThermDataResults = ThermodynamicCalculation_Results, EngForce =  EngineForce_Results)
    
    nome_file = os.path.join(output_folder, "Cranktrain Engine Forces.png")
    
    fig_EngForces.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    fig_Eng_torques = plot.Eng_torques(ThermDataResults = ThermodynamicCalculation_Results, EngForce =  EngineForce_Results)
    
    nome_file = os.path.join(output_folder, "Cranktrain Engine Torque.png")
    
    fig_Eng_torques.savefig(nome_file, dpi=300, bbox_inches="tight")
    
    report_generation(EngineData = BaseEngineData, ThermData = ThermodynamicData,
                              PreCalc = PreliminaryCalculation_Results,
                              ThermDataResults = ThermodynamicCalculation_Results,
                              EngForce = EngineForce_Results
                              )
        
if __name__ == "__main__":
    main()
