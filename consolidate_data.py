import os
import pandas as pd
from datetime import datetime

# List all files in the current working directory
files = os.listdir()

# Filter out the .csv files
csv_files = [file for file in files if file.endswith('.csv')]

# Read each CSV file and store them in a list
dfs = [pd.read_csv(file) for file in csv_files]

current_date = datetime.now().strftime('%m%d%Y')

# Create a new Excel writer object
writer = pd.ExcelWriter(f"Consolidated System Access Information - {current_date}.xlsx", engine='xlsxwriter')

# Write each dataframe to a separate sheet in the Excel file, naming sheets after the filename
for i, df in enumerate(dfs):
    # Extract file name without the extension and use it as sheet name
    sheet_name = csv_files[i].rsplit('.', 1)[0]
    df.to_excel(writer, sheet_name=sheet_name, index=False)

# Save the Excel file
# writer.save()

# Ensure to close the writer object to avoid any warnings or errors
writer.close()

# Note: The 'FutureWarning' regarding the 'save' method in this context is specific to the version of pandas and xlsxwriter used in the example execution. 
# In a standard environment, make sure your libraries are up to date to minimize such warnings. Additionally, always close the ExcelWriter to release resources.