import pandas as pd

# Read the RM file
df_UDSC = pd.read_csv('matrix_data.csv')

# Read the krona.proc.gd.tsv file into a DataFrame
df_krona = pd.read_csv('krona.proc.gd.tsv', sep='\t', header=None, names=['Sum', 'Process', 'Module', 'KO_ID', 'Description'])

print("Original krona file")
print(df_krona.head())

#Match KO IDs with columns in df_RM and update the 'Sum' column in df_krona
for idx, row in df_krona.iterrows():
    ko_ids = row['KO_ID'].split(',')  # Split KO IDs if they are separated by commas
    sum_value = 0
    for ko_id in ko_ids:
        ko_id = ko_id.strip()  # Remove leading/trailing whitespace
        if ko_id in df_UDSC.columns:
            sum_value += df_UDSC[ko_id].sum()
    df_krona.at[idx, 'Sum'] = sum_value

print("Mapped krona file")
print(df_krona.head())

# Write the updated DataFrame back to the krona.proc.gd.tsv file
df_krona.to_csv('mapped_krona.proc.gd.tsv', sep='\t', header=False, index=False)

print("Written modified krona file to system")
