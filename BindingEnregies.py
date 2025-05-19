import pandas as pd

# Load the main file with ligands and binding affinities
main_file = pd.read_excel('filtered_compounds_1477.xlsx')

# Load the list of ligands you want to find
target_ligands = pd.read_excel('Site4Compounds.xlsx')

# Merge the DataFrames to retrieve binding affinities
# Assumes the ligand column is named 'ligand' in both files
results = pd.merge(
    target_ligands, 
    main_file, 
    on='DrugBankID', 
    how='left'
)

# Save the results
results.to_excel('Site4_binding_affinities.xlsx', index=False)

print(f"Total ligands searched: {len(target_ligands)}")
print(f"Ligands found: {len(results[results['DrugBankID'].notna()])}")

