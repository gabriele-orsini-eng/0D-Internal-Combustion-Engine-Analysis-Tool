#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:59:57 2026

@author: gabriele
"""

import pandas as pd
from dataclasses import dataclass

@dataclass
class BaseEngineData:
    total_displacement: float
    cylinders_number: int
    bank_angle_deg: float
    piston_stroke_mm: float
    piston_bore_mm: float
    crank_radius_mm: float
    external_pin_diameter_mm: float
    piston_area: float
    counterweight_radius_mm: float
    piston_support_width_mm: float
    connecting_rod_length_mm: float
    max_engine_speed_rpm: float
    volumetric_efficiency: float
    intake_pressure_bar: float
    intake_temperature_deg: float
    engine_cycle: int
    intakevalve_discharge_coefficient: float
    mach_coefficient: float
    temperature_coefficient_sound: float
    piston_compression_height_mm : float
    number_intake_valves: int
    number_exhaust_valves: int

def read_excel_BaseEngineData(filename):
    df_BaseEngineData = pd.read_excel(filename, sheet_name="Base Engine Data")
    df_BaseEngineData.set_index("Parameter", inplace=True)
    
    return BaseEngineData(
        total_displacement = df_BaseEngineData.loc["Total Displacement", "Value"],
        cylinders_number = df_BaseEngineData.loc["Cylinders Number", "Value"],
        bank_angle_deg = df_BaseEngineData.loc["Bank Angle", "Value"],
        piston_stroke_mm = df_BaseEngineData.loc["Piston Stroke", "Value"],
        piston_bore_mm = df_BaseEngineData.loc["Piston Bore", "Value"],
        crank_radius_mm = df_BaseEngineData.loc["Crank Radius", "Value"],
        piston_area = df_BaseEngineData.loc["Piston Area", "Value"],
        external_pin_diameter_mm = df_BaseEngineData.loc["External Pin Diameter", "Value"],
        counterweight_radius_mm = df_BaseEngineData.loc["Counterweight Radius", "Value"],
        piston_support_width_mm = df_BaseEngineData.loc["Piston Support Width", "Value"],
        connecting_rod_length_mm = df_BaseEngineData.loc["Connecting Rod Length", "Value"],
        max_engine_speed_rpm = df_BaseEngineData.loc["Max Engine Speed", "Value"],
        volumetric_efficiency = df_BaseEngineData.loc["Volumetric Efficiency", "Value"],
        intake_pressure_bar = df_BaseEngineData.loc["Intake Pressure", "Value"],
        intake_temperature_deg = df_BaseEngineData.loc["Intake Temperature", "Value"],
        engine_cycle = df_BaseEngineData.loc["Engine Cycle", "Value"],
        intakevalve_discharge_coefficient = df_BaseEngineData.loc["Intake Valve Discharge Coefficient", "Value"],
        mach_coefficient = df_BaseEngineData.loc["Mach Coefficient", "Value"],
        temperature_coefficient_sound = df_BaseEngineData.loc["Temperature Coefficient Sound", "Value"],
        piston_compression_height_mm = df_BaseEngineData.loc["Piston Compression Height", "Value"],
        number_intake_valves = df_BaseEngineData.loc["Number of Intake Valves", "Value"],
        number_exhaust_valves = df_BaseEngineData.loc["Number of Exhaust Valves", "Value"]
        )

@dataclass
class ThermodynamicData:
    compression_ratio: float
    polytropic_coeff_compression: float
    polytropic_coeff_combustion: float
    polytropic_coeff_expansion: float
    counter_pressure_carter_bar: float
    exhaust_pressure_bar: float
    exhaust_temperature_deg: float
    start_combustion_angle_deg: float
    end_combustion_angle_deg: float
    low_heating_value: float
    fuel_metering: float
    wiebe_efficiency_factor: float
    wiebe_shape_factor: float
    lambda_engine: float
    engine_total_efficiency: float
    engine_adiabatic_efficiency: float
    engine_combustion_efficiency: float
    engine_pumping_efficiency: float
    engine_mechanical_efficiency: float
    pressure_scaling: int
    pfp: float
  

    
def read_excel_Thermodynamic(filename):
    df_ThermodynamicData = pd.read_excel(filename, sheet_name="Thermodynamic")
    df_ThermodynamicData.set_index("Parameter", inplace=True)
    
    return ThermodynamicData(
       compression_ratio = df_ThermodynamicData.loc["Compression Ratio", "Value"], 
       polytropic_coeff_compression = df_ThermodynamicData.loc["Polytropic Compression Coefficient", "Value"],
       polytropic_coeff_combustion = df_ThermodynamicData.loc["Polytropic Combustion Coefficient", "Value"],
       polytropic_coeff_expansion = df_ThermodynamicData.loc["Polytropic Expansion Coefficient", "Value"],
       counter_pressure_carter_bar = df_ThermodynamicData.loc["Counter Pressure Carter", "Value"],
       exhaust_pressure_bar = df_ThermodynamicData.loc["Exhaust Pressure", "Value"],
       exhaust_temperature_deg = df_ThermodynamicData.loc["Exhaust Temperature", "Value"],
       start_combustion_angle_deg = df_ThermodynamicData.loc["Start of Combustion Angle", "Value"],
       end_combustion_angle_deg = df_ThermodynamicData.loc["End of Combustion Angle", "Value"],
       low_heating_value = df_ThermodynamicData.loc["Low Heating Value", "Value"],
       fuel_metering = df_ThermodynamicData.loc["Fuel Metering", "Value"],
       wiebe_efficiency_factor = df_ThermodynamicData.loc["Wiebe Efficiency factor", "Value"],
       wiebe_shape_factor = df_ThermodynamicData.loc["Wiebe Shape Factor", "Value"],
       lambda_engine = df_ThermodynamicData.loc["Lambda", "Value"],
       engine_total_efficiency= df_ThermodynamicData.loc["Engine Total Efficiency", "Value"],
       engine_adiabatic_efficiency = df_ThermodynamicData.loc["Engine Adiabatic Efficiency", "Value"],
       engine_combustion_efficiency = df_ThermodynamicData.loc["Engine Combustion Efficiency", "Value"],
       engine_pumping_efficiency = df_ThermodynamicData.loc["Engine Pumping Efficiency", "Value"],
       engine_mechanical_efficiency = df_ThermodynamicData.loc["Engine Mechanical Efficiency", "Value"],
       pressure_scaling = df_ThermodynamicData.loc["Pressure Scaling", "Value"],
       pfp = df_ThermodynamicData.loc["New Peak Firing Pressure", "Value"]
       )


@dataclass
class Cranktrain_Masses:
    conrod_assembly_mass_g: float
    bushing_mass_g: float
    piston_mass_g: float
    seg_1_mass_g: float
    seg_2_mass_g: float
    seg_oil_mass_g: float
    piston_pin_mass_g: float
    pin_ring_mass_g: float
    conrod_pin_mass_g: float
    cog_conrod_mm: float
    cog_main_bearing_mm: float
    
def read_excel_cranktrain_masses(filename):
    df_Cranktrain_Masses = pd.read_excel(filename, sheet_name="Cranktrain Mass")
    df_Cranktrain_Masses.set_index("Parameter", inplace=True)
    
    return Cranktrain_Masses(
        conrod_assembly_mass_g = df_Cranktrain_Masses.loc["Connecting Rod Mass", "Value"],
        bushing_mass_g = df_Cranktrain_Masses.loc["Bushing Mass", "Value"],
        piston_mass_g = df_Cranktrain_Masses.loc["Piston Mass", "Value"],
        seg_1_mass_g = df_Cranktrain_Masses.loc["1° Segment Mass", "Value"],
        seg_2_mass_g = df_Cranktrain_Masses.loc["2° Segment Mass", "Value"], 
        seg_oil_mass_g = df_Cranktrain_Masses.loc["Oil Segment Mass", "Value"],
        piston_pin_mass_g = df_Cranktrain_Masses.loc["Piston Pin Mass", "Value"],
        pin_ring_mass_g = df_Cranktrain_Masses.loc["Piston Pin Ring Mass", "Value"],
        conrod_pin_mass_g = df_Cranktrain_Masses.loc["Connectig Rod Pin Mass", "Value"],
        cog_conrod_mm = df_Cranktrain_Masses.loc["Connectin Rod CoG", "Value"],
        cog_main_bearing_mm = df_Cranktrain_Masses.loc["Connecting Rod Pin CoG", "Value"]
        )