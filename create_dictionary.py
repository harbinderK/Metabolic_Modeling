import pandas as pd
import requests
import re

# Download and parse the file 
url = "https://www.genome.jp/kegg-bin/download_htext?htext=br08610&format=htext&filedir="
response = requests.get(url)

# Check if the download was successful
if response.status_code == 200:
    # Extract content from the downloaded file
    content = response.text
    pattern = r'TAX:(\d+)\]\n.\s+(\w+)'
    matches = re.findall(pattern, content)

    # Create a dictionary to store TaxID to KEGG organism name mapping
    taxid_to_org = {taxid: org_name for taxid, org_name in matches}
    df_taxid_to_org = pd.DataFrame(list(taxid_to_org.items()), columns=['TaxID', 'Organism_Name'])

    # Specify the output file path
    output_file = 'taxid_to_org.csv'

    # Save the DataFrame as a CSV file
    df_taxid_to_org.to_csv(output_file, sep='\t', index=False)

    print(f"Dictionary saved as {output_file}")

else:
    raise Exception("Failed to download the file")


