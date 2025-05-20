import pandas as pd
import matplotlib.pyplot as plt
import os

# Load your data from Excel
df = pd.read_excel('Both_Positives_Negatives_Site1.xlsx')

# Initialize a dictionary to hold residue counts for each interaction type
interaction_counts = {}

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

# Count occurrences of residues in each interaction column
for column in interaction_columns:
    if column in df.columns:
        # Split residues, explode, and strip whitespace
        residues = df[column].astype(str).str.split(',').explode().str.strip()
        
        # Remove any empty strings or specific unwanted values like 'nan'
        residues = residues[~residues.isin(['', 'nan', 'NaN', 'None'])]  # Filter out unwanted values
        
        # Debug: Check the number of residues remaining for each column
        print(f"Processing column: {column}")
        print(f"Initial number of residues: {len(residues)}")
        print(f"Valid residues (after cleaning): {len(residues)}")
        
        # Special debug for 'Unfavorable Donor-Donor/Acceptor-Acceptor'
        if column == 'Unfavorable Donor-Donor/Acceptor-Acceptor':
            print(f"Residues in '{column}':")
            print(residues.head(10))  # Print first 10 residues for inspection

        if len(residues) > 0:
            # Count residues and store in the dictionary
            interaction_counts[column] = residues.value_counts()

# Combine all counts into a single DataFrame
all_residue_counts = pd.concat(interaction_counts).groupby(level=0).sum()

# Prepare data for plotting
total_residue_counts = all_residue_counts.reset_index()
total_residue_counts.columns = ['Residue', 'Total Frequency']

# Create output directory if it doesn't exist
output_dir = '/home/bio-staff-003/Desktop/Plots/Both/Site1_Both_118'
os.makedirs(output_dir, exist_ok=True)

# Define colors for each interaction type
colors = {
    'Hydrogen bond interactions': 'skyblue',
    'pi-sigma interactions': 'salmon',
    'alkyl/pi-alkyl interactions': 'orange',
    'pi-Cation/pi-Anion': 'pink',
    'Unfavorable Donor-Donor/Acceptor-Acceptor': 'purple',
    'Halogen Interaction': 'blue',
    'Amide-pi Stacked/pi-pi Stacked': 'green'
}

# Plotting total frequency of residues across all interactions
plt.figure(figsize=(12, 6))
bars = plt.bar(total_residue_counts['Residue'], total_residue_counts['Total Frequency'], color='skyblue', width=0.6)
plt.xlabel('Residue')
plt.ylabel('Total Frequency')
plt.title('Total Frequency of Residues Across All Interactions_Both_Positives_Negatives_Site1')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Adding value labels on top of bars
plt.bar_label(bars)

# Save the plot as an image file
plt.savefig(os.path.join(output_dir, 'total_frequency_residues_Both_Positives_Negatives_Site1.png'))
plt.close()  # Close the figure to free up memory

# Now plot frequency for each interaction type with different colors
for column in interaction_columns:
    if column in df.columns:
        # Prepare data for individual interaction plots
        residue_counts = interaction_counts[column].reset_index()
        residue_counts.columns = ['Residue', 'Frequency']
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(residue_counts['Residue'], residue_counts['Frequency'], color=colors[column], width=0.6)
        plt.xlabel('Residue')
        plt.ylabel('Frequency')
        plt.title(f'Frequency of Residues in {column}_Both_Positives_Negatives_Site1')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Adding value labels on top of bars
        plt.bar_label(bars)

        # Save the plot as an image file in the output directory
        safe_column_name = column.replace('/', '_').replace(' ', '_')  # Replace spaces and slashes for safe filenames
        plt.savefig(os.path.join(output_dir, f'frequency_residues_Both_Positives_Negatives_Site1_{safe_column_name}.png'))
        plt.close()  # Close the figure to free up memory

# Create a summary plot combining all interactions with different colors
plt.figure(figsize=(14, 8))

# Create a stacked bar chart for all interactions combined by residue
for i, column in enumerate(interaction_columns):
    if column in df.columns:
        residue_counts = interaction_counts[column].reset_index()
        residue_counts.columns = ['Residue', 'Frequency']
        
        # Create a bar for each interaction type at the same x position with an offset for stacking
        plt.bar(residue_counts['Residue'], residue_counts['Frequency'], color=colors[column], label=column)

plt.xlabel('Residue')
plt.ylabel('Frequency')
plt.title('Combined Frequency of Residues Across Different Interactions_Both_Positives_Negatives_Site1')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Adding legend to describe colors used for different interactions
plt.legend(title='Interaction Types')

# Save the summary plot as an image file
plt.savefig(os.path.join(output_dir, 'combined_frequency_residues_Both_Positives_Negatives_Site1.png'))
plt.close()  # Close the figure to free up memory

print("Plots saved successfully.")
