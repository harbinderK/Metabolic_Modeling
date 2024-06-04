import pandas as pd
import requests

# Read the organism to TaxID mapping from a file

mapping_file = 'taxid_to_org.csv'
df_mapping = pd.read_csv(mapping_file, sep='\t')

# Print the columns to debug the issue
print("Columns in df_mapping:", df_mapping.columns)

# Check for the presence of 'TaxID' and 'Organism_Name' columns
if 'TaxID' not in df_mapping.columns or 'Organism_Name' not in df_mapping.columns:
    raise ValueError("Expected columns 'TaxID' and 'Organism_Name' not found in the mapping file")

# Create a dictionary to store TaxID to KEGG organism name mapping
taxid_to_org = dict(zip(df_mapping['TaxID'].astype(str), df_mapping['Organism_Name']))

# Read the taxonomy file into a pandas DataFrame
file_path = 'UDSC_uniquereads_taxidn.txt'
df_UDSC = pd.read_csv(file_path, sep='\t')

# Extract TaxIDs from the 'taxID' column and convert them to strings
taxids = df_UDSC['taxID'].astype(str).tolist()

# Retrieve genes with KO numbers for each selected organism
def get_ko_ids(organism_id):
    url = f"http://rest.kegg.jp/link/ko/{organism_id}"
    response = requests.get(url)
    ko_ids = []
    if response.status_code == 200:
        lines = response.text.strip().split("\n")
        for line in lines:
            fields = line.split("\t")
            ko_id = fields[1].split(":")[1]  # Extract KO ID
            ko_ids.append(ko_id)
    return ko_ids

# Create organism-KO matrix for Taxonomy file
matrix_data = {}

for taxid in taxids:
    organism_id = taxid_to_org.get(taxid)
    if organism_id:
        ko_ids = get_ko_ids(organism_id)
        matrix_data[organism_id] = ko_ids

# Create a set of all KO values from the matrix
all_ko_values = sorted(set(k for sublist in matrix_data.values() for k in sublist))

df = pd.DataFrame(index=matrix_data.keys(), columns=all_ko_values)

for organism_id, ko_ids in matrix_data.items():
    row = {ko: 1 if ko in ko_ids else 0 for ko in df.columns}
    df.loc[organism_id] = row

# Fill NaN values with 0 (for KO values not present in any row)
df = df.fillna(0).astype(int)

# Specify the output file path and save the DataFrame as a CSV file
output_file = 'matrix_data.csv'
df.to_csv(output_file, index=True)

# Print the resulting DataFrame and a confirmation message
print(df)
print(f"DataFrame saved as {output_file}")

