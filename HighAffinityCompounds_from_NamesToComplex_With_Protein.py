import os
import shutil
import pandas as pd
from pymol import cmd

def extract_filtered_ligands(pyrx_file, site4_file):
    pyrx_df = pd.read_excel(pyrx_file)
    site4_df = pd.read_excel(site4_file)

    # Sort PyRx results and drop duplicates
    pyrx_sorted = pyrx_df.sort_values('binding affinity', ascending=True)
    pyrx_filtered = pyrx_sorted.drop_duplicates(subset='ligand', keep='first')

    # Match with Site4 list
    merged = pd.merge(site4_df, pyrx_filtered, left_on='DrugBankID', right_on='ligand', how='inner')
    print(f"Total matched ligands: {len(merged)}")

    # Save matched list
    merged.to_excel("Filtered_Matched_HighAffinity.xlsx", index=False)
    return merged

def add_names(merged_df, name_file):
    name_map = pd.read_excel(name_file)
    merged_named = pd.merge(merged_df, name_map, on='DrugBankID', how='left')
    merged_named.to_excel("Filtered_HighAffinity_WithNames.xlsx", index=False)
    print("Names added to matched ligands.")
    return merged_named

def retrieve_pdbqt_files(matched_df, source_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ligands = set(matched_df['ligand'].astype(str))
    copied = 0

    for fname in os.listdir(source_dir):
        if fname.endswith('.pdbqt'):
            ligand_id = fname.split('_uff_')[0]
            if ligand_id in ligands:
                shutil.copy(os.path.join(source_dir, fname), os.path.join(output_dir, fname))
                copied += 1

    print(f"Retrieved {copied} .pdbqt files to: {output_dir}")

def generate_complexes(protein_pdbqt, ligand_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    cmd.reinitialize()
    cmd.load(protein_pdbqt, 'protein')

    for ligand_file in os.listdir(ligand_dir):
        if ligand_file.endswith('.pdbqt'):
            ligand_path = os.path.join(ligand_dir, ligand_file)
            cmd.load(ligand_path, 'ligand')
            out_name = os.path.join(output_dir, f"complex_{os.path.splitext(ligand_file)[0]}.pdb")
            cmd.save(out_name, 'protein or ligand')
            cmd.delete('ligand')

    cmd.delete('protein')
    print(f"Protein-ligand complexes saved in {output_dir}")

# ---------- MAIN WORKFLOW ----------
if __name__ == "__main__":
    # --- File Paths (Update as Needed) ---
    pyrx_file = "HighAffinityCompoundsPyRx.xlsx"
    site4_file = "Site4Compounds.xlsx"
    name_file = "ApprovedDrugBankIDs.xlsx"
    source_pdbqt_dir = "/path/to/all_pdbqt_files"  # <-- UPDATE THIS
    protein_file = "protein.pdbqt"
    filtered_pdbqt_dir = "HighAffinityLigands"
    complex_output_dir = "protein_ligand_complexes_pymol"

    # Step 1: Get filtered ligands matched with reference
    matched_ligands = extract_filtered_ligands(pyrx_file, site4_file)

    # Step 2: Add names
    matched_named = add_names(matched_ligands, name_file)

    # Step 3: Retrieve .pdbqt files
    retrieve_pdbqt_files(matched_named, source_pdbqt_dir, filtered_pdbqt_dir)

    # Step 4: Generate PyMOL complexes
    generate_complexes(protein_file, filtered_pdbqt_dir, complex_output_dir)

