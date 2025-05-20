import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# Load your data from Excel
df = pd.read_excel('Both_Positives_Negatives_Site1.xlsx')

# Initialize a dictionary to hold residues and their associated compounds
residue_compound_counts = {}

# List of interaction columns based on your description
interaction_columns = [
    'Hydrogen bond interactions',
    'pi-sigma interactions',
    'alkyl/pi-alkyl interactions',
    'pi-Cation/pi-Anion',
    'Unfavorable Donor-Donor/Acceptor-Acceptor',
    'Halogen Interaction',
    'Amide-pi Stacked/pi-pi Stacked'
]

# Iterate over each interaction column to count unique compounds for each residue
for column in interaction_columns:
    if column in df.columns:
        for index, row in df.iterrows():
            # Get the list of residues for this interaction
            residues = row[column]
            if isinstance(residues, str):  # Check if it's a string
                residues = residues.split(',')
                residues = [residue.strip() for residue in residues if residue.strip()]  # Clean up whitespace
                
                # Get the compound identifier (assuming it's in the second column)
                compound_id = row['PubChem_CID']  # Change this if your identifier is in another column
                
                for residue in residues:
                    if residue not in residue_compound_counts:
                        residue_compound_counts[residue] = set()  # Use a set to avoid duplicates
                    residue_compound_counts[residue].add(compound_id)  # Add compound ID to the set

# Convert sets to counts of unique compounds per residue
residue_counts = {residue: len(compounds) for residue, compounds in residue_compound_counts.items()}

# Prepare data for plotting
residue_counts_df = pd.DataFrame(residue_counts.items(), columns=['Residue', 'Unique Compounds'])

# Function to extract numeric part from residue names for sorting
def extract_numeric(residue):
    match = re.search(r'(\d+)', residue)
    return int(match.group(1)) if match else float('inf')  # Return a large number if no match

# Sort the DataFrame by the extracted numeric values in ascending order
residue_counts_df.sort_values(by='Residue', key=lambda x: x.map(extract_numeric), inplace=True)

# Create output directory if it doesn't exist
output_dir = '/home/bio-staff-003/Desktop/Plots/Both/Site1_Both_118'
os.makedirs(output_dir, exist_ok=True)

# Plotting the number of unique compounds for each residue
plt.figure(figsize=(14, 8))
bars = plt.bar(residue_counts_df['Residue'], residue_counts_df['Unique Compounds'], color='skyblue')
plt.xlabel('Residue')
plt.ylabel('Number of Unique Compounds')
plt.title('Number of Unique Compounds Associated with Each Compound in Both_Positives_Negatives_Site1')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Adding value labels on top of bars
plt.bar_label(bars)

# Save the plot as an image file
plt.savefig(os.path.join(output_dir, 'unique_compounds_per_residue_Both_Positives_Negatives_Site1.png'))
plt.close()  # Close the figure to free up memory

print("Plot saved successfully.")

