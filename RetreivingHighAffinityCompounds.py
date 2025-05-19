import os
import shutil
import pandas as pd

# Define paths
source_dir = "/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/Approved/ALLPyrxResultsFilteredHighAffinity/"
output_dir = "/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/Approved/ALLPyrxResultsFilteredHighAffinity/Filtered_HighAffinityCompounds"
ligand_file_path = "/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/Approved/ALLPyrxResultsFilteredHighAffinity/Filtered_HighAffinityCompounds.xlsx"
tracking_output_path = "/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/Approved/ALLPyrxResultsFilteredHighAffinity/Compound_Retrieval_Tracking.xlsx"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Read ligand data
try:
    ligand_data = pd.read_excel(ligand_file_path)
    ids_to_match = set(str(id).strip() for id in ligand_data['ligand'].dropna().unique())
    print(f"Total unique ligands to match: {len(ids_to_match)}")
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Retrieve matching files with detailed tracking
matching_files_info = []
for filename in os.listdir(source_dir):
    if filename.endswith('.pdbqt'):
        # Extract the exact prefix before '_uff_'
        base_filename = filename.split('_uff_')[0]
        
        # Exact matching strategy
        if base_filename in ids_to_match:
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(output_dir, filename)
            
            try:
                shutil.copy(source_file, destination_file)
                matching_files_info.append({
                    'Compound_ID': base_filename,
                    'Filename': filename,
                    'Energy_Value': filename.split('_uff_E=')[1].split('_out.pdbqt')[0]
                })
            except Exception as e:
                print(f"Error copying {filename}: {e}")

# Create tracking DataFrame
tracking_df = ligand_data.copy()

# Count files for each compound
file_count_df = pd.DataFrame(matching_files_info)
compound_file_counts = file_count_df.groupby('Compound_ID').size().reset_index(name='Retrieved_Files_Count')

# Merge with original tracking DataFrame
tracking_df = tracking_df.merge(compound_file_counts, left_on='ligand', right_on='Compound_ID', how='left')
tracking_df['Retrieved_Files_Count'] = tracking_df['Retrieved_Files_Count'].fillna(0).astype(int)
tracking_df['Retrieved'] = tracking_df['Retrieved_Files_Count'] > 0
tracking_df['Retrieval_Status'] = tracking_df['Retrieved'].map({True: 'Retrieved', False: 'Not Retrieved'})

# Reorder columns
tracking_df = tracking_df[['ligand', 'Retrieved_Files_Count', 'Retrieved', 'Retrieval_Status'] + 
                          list(tracking_df.columns[:-4])]

# Save tracking Excel
with pd.ExcelWriter(tracking_output_path) as writer:
    tracking_df.to_excel(writer, sheet_name='Compound_Tracking', index=False)
    tracking_df[tracking_df['Retrieved']].to_excel(writer, sheet_name='Retrieved_Compounds', index=False)
    tracking_df[~tracking_df['Retrieved']].to_excel(writer, sheet_name='Not_Retrieved_Compounds', index=False)

print(f"Total files copied: {len(matching_files_info)}")
print(f"Retrieved files are saved in: {output_dir}")
print(f"Tracking Excel created at: {tracking_output_path}")
print(f"Retrieved Compounds: {tracking_df['Retrieved'].sum()}")
print(f"Not Retrieved Compounds: {len(tracking_df) - tracking_df['Retrieved'].sum()}")

