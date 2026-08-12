# Engine-validation-tool

A modular Python tool for the preliminary analysis of internal combustion engines (ICE). The Python script reads geometric and operation parameters from an Excel file and automatically generates a detailed technical report.

## ℹ️ Included Features
* **InputData**: Automatic reading of data from an Excel file
* **PreliminaryCalculation**: Calculation of additional useful data for the subsequent steps such as the mean piston speed
* **Thermodynamic**: Calculation of the thermodynamic cycle and in-cylinder pressure
* **Pressure_scaling**: Scaling of the in-cylinder pressure curve as a function of a new peak firing pressure (PFP) target
* **Engine_force**: Calculation of the kinematic and dynamic relative to the piston motion
* **Plot**: Automatic generation of graphs
* **Report**: Automatic generation of a report including the main results and most important graphs

## ⚠️ Additional Features (PDF Preview)
The code structure is designed to accommodate more advanced structural analysis modules.
It is possible to examine the file `output_examples/Full_Engine_Report.pdf` to visualize the additional results generated via the following modules:
* **Material**: Calculation of additional data useful for the structural analysis.
* **ValveDynamic_Cynematic**: Calculation of the valve motion, speed and acceleration through 4 different laws. In additon to that it allows to study the lobe undercut and verify if a single spring is suitable for this application
* **PistonCalculation**: Geometry calculation and structural verification of the piston
* **PistonRing**: Geometry calculation and structural verification of piston compression ring
* **PistonPinCalculation**: Geometry calculation and structural verification of piston pin

## 📊 Roadmap
The code will be further developed with the following modules:
- [ ] Connencting rod and bolt verification
- [ ] Liners verification
- [ ] Crankshaft Structural and Torsional validation
- [ ] MOFT Calculation
<br>
For organizational purposes:
- [ ] Adoption of the PEP8 standard
- [ ] Modular approach for the report

## 🛠️ Installation & Use
1. Clone the repository
2. Install the following dependencies: `pip install -r requirements.txt`
3. Open `templates/template_input.xlsx` and insert the required data
4. Launch the main script: `python main.py`
