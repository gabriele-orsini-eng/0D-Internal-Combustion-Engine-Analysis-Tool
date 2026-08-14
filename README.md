# Engine-validation-tool

A modular Python tool for the preliminary 0D thermodynamic and cranktrain analysis of internal combustion engines (ICE).

The tool processes geometric and operating parameters from an Excel template and automatically performs preliminary calculations, engine force analysis, engineering checks, visualization, and technical report generation.

> **Project purpose:** This is a personal engineering and learning project, developed to strengthen my understanding of preliminary internal combustion engine calculations while improving my Python skills. It is not intended to replace detailed commercial simulation or design tools.

---

## Overview

The purpose of this project is to provide a fast and parametrical starting point for the preliminary analysis of an internal combustion engine before moving to more detailed simulation methods.

The workflow is designed around a simple principle:

**Input → Calculation → Verification → Visualization → Report**

The user provides the engine parameters through an Excel template. The Python modules then perform the required calculations and automatically generate plots and a technical report.

This approach allows different engine configurations and operating conditions to be investigated without modifying the calculation code directly.

---

## ℹ️​ Main Features

### Input

- Excel-based input template
- Engine geometric parameters
- Operating conditions
- Thermodynamic parameters
- Cranktrain masses
- Configurable calculation options

### Preliminary Calculations

- Engine geometric calculations
- Displacement and compression ratio
- Basic engine performance parameters
- Preliminary component sizing

### 0D Thermodynamic Analysis

- Cylinder volume throughout the engine cycle
- Pressure evolution
- Combustion modelling
- Indicating diagram
- Indicated work and performance parameters
- Pressure scaling to a target peak firing pressure

### Cranktrain Analysis

- Piston kinematics
- Gas forces
- Inertial forces
- Resulting engine/cranktrain forces
- Crankshaft torque

### Engineering Checks

The generated report includes preliminary checks of selected engine components and operating parameters.

Results are automatically highlighted according to predefined limits or design criteria.

These checks are intended as **preliminary engineering assessments**, rather than detailed component certification or final design validation.

### Automated Visualization and Reporting

The calculation process automatically generates:

- Cylinder pressure plots
- Indicating diagrams
- Pressure-scaled diagrams
- Cranktrain force plots
- Engine torque plots
- Calculation tables
- Engineering check tables
- Automatically generated technical report

---

## Workflow

```text
                 ┌──────────────────┐
                 │  Excel Template  │
                 │  Engine Inputs   │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │  Preliminary     │
                 │  Calculations    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │ 0D Thermodynamic │
                 │ Model            │
                 └────────┬─────────┘
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
       ┌────────────────┐   ┌────────────────┐
       │ Pressure       │   │ Cranktrain     │
       │ Scaling        │   │ Forces         │
       └────────────────┘   └───────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Engineering     │
                           │ Checks          │
                           └────────┬────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                 ┌──────────────┐      ┌──────────────┐
                 │ Plots        │      │ PDF Report   │
                 └──────────────┘      └──────────────┘



---

## 📊 Roadmap
The code will be further developed with the following modules:
- [ ] Connencting rod and bolt verification
- [ ] Liners verification
- [ ] Crankshaft Structural and Torsional validation
- [ ] MOFT Calculation
- [ ] Adoption of the PEP8 standard
- [ ] Modular approach also for the report

---

## 🛠️ Installation & Use
1. Clone the repository
2. Install the following dependencies: `pip install -r requirements.txt`
3. Open `templates/template_input.xlsx` and insert the required data
4. Launch the main script: `python Main.py`
