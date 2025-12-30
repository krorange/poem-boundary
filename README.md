# A Dataset of American Poetry by Poets from Historically Underrepresented Groups in the HathiTrust Digital Library

## How to download our poem section data in an HathiTrust Research Center (HTRC) Data Capsule
1. Create an HTRC Data Capsule at <https://analytics.hathitrust.org/staticcapsules>
2. Connect via remote desktop. Make sure that you are in maintenance mode.
3. Open a web browser in the remote desktop. Download `poem-boundary.py` and folders: `aa_poets`, `na_poets`, `lxa_poets`, `apa-pa_poets`, `apa-aa_poets`.
4. Switch to secure mode
5. Open the python script `poem-boundary.py` in the secure mode. In the script, replace the text "enter_folder_name" with the folder name for the group whose poems you want to download. Make sure to input the folder name inside the single (or double) quotes that are located on the _15th_ line of the file.
6. The downloaded folders will be located in the default directory "/media/secure_volume". You may change it in the python script. Each folder represents each poetry book, and each text file represents each poem page.
