# This is a program to download specific pages from digitized poem collections
# based on given poem boundary annotation files
# in an HTRC data capsule (https://analytics.hathitrust.org/staticcapsules).

# The dataset contains five folders that include poem files.
# The folder names are: aa_poets, apa-aa_poets, apa-pa_poets, lxa_poets, na_poets
# The poem boundary annotation files are in CSV format.
# The poem pages are in TXT format.

import pandas as pd
import subprocess
import os

# Define the folder
folder_path = '~/output/aa_poets'

# Extract the folder name from the given path
folder_name = os.path.basename(os.path.normpath(folder_path))

# Use the extracted folder name as the output folder name
output_folder = folder_name

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to generate the boundary range
def boundary(st, ed):
    return list(range(st, ed + 1))

# Loop through each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Extract the file name for use in the command
        csv_name = os.path.splitext(file_name)[0]

        # Check if the necessary columns exist in the CSV
        if 'File Name (start)' in df.columns and 'File Name (end)' in df.columns:
            all_file_numbers = []
            for st, ed in zip(df['File Name (start)'], df['File Name (end)']):
                if pd.notna(st) and pd.notna(ed):
                    try:
                        st = int(st)
                        ed = int(ed)
                        all_file_numbers.extend(boundary(st, ed))
                    except ValueError:
                        print(f"Skipping invalid range: start={st}, end={ed} in file {csv_name}")
            
            # Remove duplicates and sort the file numbers
            all_file_numbers = sorted(set(all_file_numbers))
            
            # Construct the output directory path for this particular CSV file
            csv_output_dir = os.path.join(output_folder, csv_name)
            
            # Generate the htrc download command
            command = f"htrc download -o /media/secure_volume/{csv_name} -pg {csv_name}[{','.join(map(str, all_file_numbers))}]"
            
            # Print the command
            print(f"Executing: {command}")
            
            # Attempt to run the command
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Command failed for {csv_name}. Skipping.")
        else:
            print(f"Skipping {file_name}: required columns not found")
