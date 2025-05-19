import os
import pymol
from pymol import cmd

def process_ligand_protein_complexes(protein_pdbqt, ligand_pdbqt_dir):
    # Create a new folder for complex PDB files
    output_dir = 'protein_ligand_complexes_pymol'
    os.makedirs(output_dir, exist_ok=True)

    # Load target protein
    cmd.load(protein_pdbqt, '3D34')

    # Iterate through ligand files
    for ligand_file in os.listdir(ligand_pdbqt_dir):
        if ligand_file.endswith('.pdbqt'):
            # Full path to ligand
            ligand_path = os.path.join(ligand_pdbqt_dir, ligand_file)
            
            # Load ligand
            cmd.load(ligand_path, 'ligand')
            
            # Generate output filename
            output_filename = os.path.join(output_dir, f'complex_{os.path.splitext(ligand_file)[0]}.pdb')
            
            # Save complex
            cmd.save(output_filename, selection='3D34 or ligand')
            
            # Clean up ligand
            cmd.delete('ligand')

    # Optional: Clean up protein
    cmd.delete('target_protein')

# Example usage
protein_pdbqt = '3D34.pdbqt'
ligand_pdbqt_dir = '/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/RemainingDrugBankIDs/RemainingDrugBankCompounds/DockingResults337/DockingWith10Poses/HighAffinityCompounds215From337'
process_ligand_protein_complexes(protein_pdbqt, ligand_pdbqt_dir)

