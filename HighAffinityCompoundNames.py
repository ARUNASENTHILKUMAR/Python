import pandas as pd

# Input file paths
file1_path = "ApprovedDrugBankIDs.xlsx"
file2_path = "Site4Compounds.xlsx"

# Load the files
file1 = pd.read_excel(file1_path)
file2 = pd.read_excel(file2_path)

# Rename columns if needed
file2 = file2.rename(columns={'ligand': 'DrugBankID'})

# Merge the DataFrames
merged = pd.merge(file2, file1, on='DrugBankID', how='left')

# Save the result
output_file = "Site4Names.xlsx"
merged.to_excel(output_file, index=False)

print(f"Matched compounds saved to {output_file}")

