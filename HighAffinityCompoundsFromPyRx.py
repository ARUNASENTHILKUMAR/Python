import pandas as pd

# Read the Excel file
df = pd.read_excel('/home/bio-staff-005/Downloads/Mindin/Compounds/Docking/DrugBank/Approved/ALLPyrxResultsFilteredHighAffinity/Filtered_HighAffinityCompounds/HighAffinityCompoundsPyRx.xlsx')

# Sort the DataFrame by binding affinity (ascending order for negative values)
# This ensures most negative (lowest) values are prioritized
df_sorted = df.sort_values('binding affinity', ascending=True)

# Remove duplicates, keeping the first occurrence (most negative value)
df_filtered = df_sorted.drop_duplicates(subset='ligand', keep='first')

# Save the result
df_filtered.to_excel('filtered_compounds.xlsx', index=False)

print(f"Total original entries: {len(df)}")
print(f"Unique compounds after filtering: {len(df_filtered)}")

