# Bioinformatics Scripts Collection

This repository comprises Python scripts developed for various bioinformatics tasks, including molecular docking analyses, data extraction, and processing of PyRx outputs.

## Scripts Overview

- BindingEnergies.py: Calculates binding energies from docking results.
- HighAffinityCompoundNames.py: Extracts names of compounds with high binding affinity.
- HighAffinityCompoundsFromPyRx.py: Processes PyRx output files to identify top compounds.
- HighAffinityCompounds_from_NamesToComplex_With_Protein.py: Maps compound names to protein complexes.
- PDBComplex.py: Handles PDB file manipulations and complex formations.
- RetrievingHighAffinityCompounds.py: Automates retrieval of high-affinity compounds.

## Technologies Used

- Python 3.x
- pandas
- Biopython
- NumPy

##  How to Use

1. Clone the repository:
   bash
   git clone https://github.com/ARUNASENTHILKUMAR/Python.git
   cd Python

2. Install required packages:
   pip install -r requirements.txt

3. Run desired scripts:
   python BindingEnergies.py
