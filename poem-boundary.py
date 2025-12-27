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

# Define the folder containing the CSV files
# The default path is: '/home/dcuser/Downloads/...'
# Select one folder among 'aa_poets', 'apa-aa_poets', 'apa-pa_poets', 'lxa_poets', 'na_poets'
folder_path = '/home/dcuser/Downloads/aa_poets'

# Extract the folder name from the given path
folder_name = os.path.basename(os.path.normpath(folder_path))

# Use the extracted folder name as the output folder name
output_folder = folder_name + '_annotations'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the skipped file name
skipped_file_name = f"skipped_{folder_name}.txt"

# Function to generate the boundary range
def boundary(st, ed):
    return list(range(st, ed + 1))

# Keep track of skipped CSV names (volume IDs)
skipped_names = []

# Loop through each CSV file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Construct the full path to the CSV file
        file_path = os.path.join(folder_path, file_name)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Extract the file name without extension
        csv_name = os.path.splitext(file_name)[0]

        # Check if the necessary columns exist in the CSV
        if 'File Name (start)' in df.columns and 'File Name (end)' in df.columns:
            # Collect all ranges into a single list
            all_file_numbers = []

            for st, ed in zip(df['File Name (start)'], df['File Name (end)']):
                if pd.notna(st) and pd.notna(ed):
                    try:
                        # Convert to integer and generate the range for each row
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
            pages_str = ",".join(map(str, all_file_numbers))
            command = f"htrc download -o {csv_output_dir} -pg {csv_name}[{pages_str}]"
            
            # Print the final command
            print(f"Executing: {command}")

            # Attempt to run the command
            try:
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                # If the command fails, print an error and skip this CSV file
                print(f"Command failed for {csv_name}. Skipping.")
                skipped_names.append(f"{csv_name}[{pages_str}]")

        else:
            print(f"Skipping {file_name}: required columns not found".)

# Create a text file for skipped CSV names
if skipped_names:
    with open(skipped_file_name, "w") as f:
        for name in skipped_names:
            f.write(name + "\n")
        print(f"Skipped CSV names written to {skipped_file_name}")
else:
    print("No CSV names were skpped.")
