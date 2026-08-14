#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 19:01:02 2026

@author: gabriele
"""


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.platypus import PageBreak
from reportlab.lib import colors
from modules.InputData import BaseEngineData
from modules.PreliminaryCalculation import PreliminaryCalculation_Results
from modules.InputData import ThermodynamicData
from modules.Thermodynamic import ThermodynamicCalculation_Results
from modules.Pressure_scaling import PressureScaling_Results
from modules.Engine_force import EngineForce_Results

def report_generation(EngineData: BaseEngineData, ThermData: ThermodynamicData,
                      PreCalc: PreliminaryCalculation_Results,
                      ThermDataResults: ThermodynamicCalculation_Results,
                      EngForce: EngineForce_Results,
                      filename="Engine_Evaluation.pdf"):
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'Main Title',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"), 
        spaceAfter=20
    )
    
    # Subtitle style
    subtitle_style = ParagraphStyle(
        'Sub-title',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True 
    )
    
    # Body Text
    body_style = ParagraphStyle(
        'Text',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=4, 
        spaceAfter=10
    )

    # Story
    story = []
    
    # First Page
    story.append(Paragraph("Engine Evaluation Tool - Technical Report", title_style))
    story.append(Spacer(1, 15)) # Vertical Space
    story.append(PageBreak())
    
    # Index
    story.append(Paragraph("1. Project General Description", subtitle_style))
    story.append(Paragraph("2. Base Engine Data", subtitle_style))
    story.append(Paragraph("3. Engine Kinematic & Thermodynamic Calculation", subtitle_style))
    story.append(Paragraph("4. Cranktrain Engine Forces & Torque", subtitle_style))
    story.append(PageBreak())
    
    # General Part
    story.append(Paragraph("1.1 Project General Description", subtitle_style))
    story.append(Spacer(1, 15))
    testo_intro = (
        "This calculation tool was developed in Python with the aim of automating "
        "the preliminary evaluation of an internal combustion engine. "
        "This code takes a dedicated Excel template file as input and, using internal formulas "
        "and an object (Dataclasses) oriented approach, provides an estimation "
        "of the engine performances and a verification of the critical sections of its components."
    )
    story.append(Paragraph(testo_intro, body_style))
    
    # code architecture
    story.append(Paragraph("1.2 Code and Modules architecture", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The software architecture is divided in the following sections to "
        "retain a better scalability and easy maintenance in the future:"
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    dati_tabella = [
        [Paragraph("<b>Module</b>", body_style), Paragraph("<b>Functional Description</b>", body_style)],
        ["InputData.py", "Input data management"],
        ["PreliminaryCalculation.py", "Main engine data calculation including mean engine speed and valve diameter"],
        ["Main.py", "Main script that manage modules, calculation and report generation"],
        ["Thermodynamic.py", "Kinematic and Thermodynamic calculation"],
        ["Pressure_scaling.py", "Scaling of the pressure curve as a function of the new PFP"],
        ["Engine_force.py", "Kinematic and Dynamic calculation of the piston motion"],
        ["Plot.py", "Automatic generation of graphs"],
        ["Report.py", "Automatic generation of a technical report"],
    ]
    
    tabella = Table(dati_tabella, colWidths=[150, 350])
    tabella.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#1A365D")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    ]))
    
    story.append(tabella)
    story.append(Spacer(1, 20))
    
    # Sezione Note
    story.append(Paragraph("1.3 Notes", subtitle_style))
    story.append(Spacer(1, 15))
    testo_note = (
        "This tool requires the following Python libraries: Dataclasses, Numpy, Pandas, Matplotlib and ReportLab "
    )
    story.append(Paragraph(testo_note, body_style))
    story.append(PageBreak())
    
    # Base Engine Data
    story.append(Paragraph("2.1 Base Engine Data", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The Base Engine Data are reported in the following table: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    dati_tabella = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style), Paragraph("<b>Unit</b>", body_style)],
        ["Engine Displacement", f"{EngineData.total_displacement:.1f}", "cm3"],
        ["Engine Cycle", f"{EngineData.engine_cycle:.0f}", "-"],
        ["Number of Cylinders", f"{EngineData.cylinders_number:.0f}", "-"],
        ["Piston Stroke", f"{EngineData.piston_stroke_mm:.1f}", "mm"],
        ["Piston Bore", f"{EngineData.piston_bore_mm:.1f}", "mm"],
        ["Engine Speed @ Maximum Power", f"{EngineData.max_engine_speed_rpm:.0f}", "RPM"]
        ]
    
    
    tabella = Table(dati_tabella, colWidths=[300, 100, 100])
    tabella.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#1A365D")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    ]))
    
    story.append(tabella)
    story.append(Spacer(1, 20))
    
    # Additional Engine Data
    story.append(Paragraph("2.2 Additional Engine Data", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The following data are needed to further define the engine: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    dati_tabella = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style), Paragraph("<b>Unit</b>", body_style)],
        ["Mean Piston Speed", f"{PreCalc.mean_piston_speed_ms:.1f}", "m/s"],
        ["Number of Intake Valves", f"{EngineData.number_intake_valves:.0f}", "-"],
        ["Number of Exhaust Valves", f"{EngineData.number_exhaust_valves:.0f}", "-"],
        ["Intake Valve Diameter", f"{PreCalc.intakevalve_diameter_mm:.1f}", "mm"],
        ["Exhaust Valve Diameter", f"{PreCalc.exhaustvalve_diameter_mm:.1f}", "mm"],
        ]
    
    
    tabella = Table(dati_tabella, colWidths=[300, 100, 100])
    tabella.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#1A365D")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    ]))
    
    story.append(tabella)
    story.append(Spacer(1, 20))
    story.append(PageBreak())
    
    story.append(Paragraph("2.2 Engine Thermodynamic Data", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The in-cylinder pressure computed by the Wiebe function is the following: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    img_path = "output_examples/Wiebe Cylinder Pressure.png"
    image = Image(img_path, width=500, height=250)

    story.append(image)
    
    testo_architettura = (
        "The indicating cycle and useful work is depicted in the following picture: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    img_path = "output_example/Indicating Diagram.png"
    image = Image(img_path, width=500, height=250)

    story.append(image)
    story.append(PageBreak())
    
    testo_architettura = (
        "The table reports the general engine performance data: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    dati_tabella = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style), Paragraph("<b>Unit</b>", body_style)],
        ["Cylinder Theorical Air Mass", f"{ThermDataResults.M_Air_Re_g:.1f}", "g"],
        ["Cylinder Fuel Mass", f"{ThermDataResults.M_Comb_g:.3f}", "g"],
        ["Cylinder Heat", f"{ThermDataResults.Q_In_J:.1f}", "J"],
        ["Engine Power", f"{ThermDataResults.P_In_kwatt:.1f}", "KW"],
        ["Engine Power", f"{ThermDataResults.P_Eff_estimated_cv:.1f}", "CV"],
        ]
    
    
    tabella = Table(dati_tabella, colWidths=[300, 100, 100])
    tabella.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")), 
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor("#1A365D")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")), 
    ]))
    
    story.append(tabella)
    story.append(Spacer(1, 20))
    story.append(PageBreak())
    
    story.append(Paragraph("3.1 Engine Performance at New Peak Firing Pressure", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The new in-cylinder pressure computed by the Wiebe function and the new indicated work are depicted in the following pictures: "
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    if int(ThermData.pressure_scaling) == 1:
        
        img_path_1 = "output_examples/Pressure Scaled to New PFP.png"
        image_1 = Image(img_path_1, width=500, height=250)
        story.append(image_1)
        
        img_path_2 = "output_examples/Indicating Diagram at New PFP.png"
        image_2 = Image(img_path_2, width=500, height=250)
        story.append(image_2)
    
    else:
        
        story.append(Paragraph("1.3 Notes", subtitle_style))
        story.append(Spacer(1, 15))
        testo_note = (
            "User Decides to NOT Scale the Pressure Curve"
        )
        story.append(Paragraph(testo_note, body_style))
        
    story.append(PageBreak())
  
    story.append(Paragraph("4.1 Cranktrain Engine Forces and Torque", subtitle_style))
    story.append(Spacer(1, 15))
    testo_architettura = (
        "The following two quantities are computed:"
        "<br/>1) The total force due to the components inertia and gas force;"
        "<br/>2) The instantaneous torque that is produced by the engine."
        "<br/> Be aware that the following data refer to a single engine cylinder."
    )
    story.append(Paragraph(testo_architettura, body_style))
    
    img_path = "output_examples/Cranktrain Engine Forces.png"
    image = Image(img_path, width=500, height=250)
    story.append(image)

    img_path = "output_examples/Cranktrain Engine Torque.png"
    image = Image(img_path, width=500, height=250)
 
    story.append(image)
    story.append(PageBreak())

    doc.build(story)
    
if __name__ == "__main__":
    report_generation()
  
