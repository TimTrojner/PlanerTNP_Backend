import pandas as pd
import os

# Define download directory and file path
download_dir = os.path.abspath("../downloads")
files = os.listdir(download_dir)

# List files for the user
print("\nAvailable Files:")
for index, file in enumerate(files):
    print(f"{index + 1}. {file}")

# 4. Prompt the user to choose an index
while True:
  try:
    # target_index = int(input("\nEnter the number corresponding to your desired option: "))
    target_index=1
    target_index-=1
    if 0 <= target_index <= len(files):
      break
    else:
      print(f"Please enter a number between 1 and {len(files)}")
  except ValueError:
    print("Invalid input. Please enter a number.")


# Simulate user selection of the file
file_path = os.path.join(download_dir, files[target_index])


# Output CSV path
output_csv = file_path.replace('.xls', '_google_calendar.csv')


# Load and convert the Excel file
try:
    print("reading file")
    # Read Excel file
       # Read the Excel file, skipping the first 3 rows
    df = pd.read_excel(file_path, skiprows=3, engine='xlrd', usecols="C,D,E,F,H,J",
                       names=['datum', 'ura', 'prostor', 'izvajanje', 'skupina', 'izvajalec'])

    print("File read successfully.")

    # Extract start and end times from 'ura' column
    start_times = df['ura'].str.split('-', expand=True)[0]
    end_times = df['ura'].str.split('-', expand=True)[1]

    # Map columns to Google Calendar format
    google_calendar_df = pd.DataFrame({
        'Subject': df['izvajanje'],
        'Start Date': pd.to_datetime(df['datum'], format='%d.%m.%Y').dt.strftime('%m/%d/%Y'),  # Correct format
        'Start Time': start_times,
        'End Date': pd.to_datetime(df['datum'], format='%d.%m.%Y').dt.strftime('%m/%d/%Y'),  # Correct format
        'End Time': end_times,
        'All Day Event': 'FALSE',
        'Description': df['skupina'] + ' - ' + df['izvajalec'],
        'Location': df['prostor'],
        'Private': 'FALSE'
    })

    print("Converting to Google Calendar CSV format...")

    # Save to CSV
    google_calendar_df.to_csv(output_csv, index=False)
    print(f"File successfully converted and saved to: {output_csv}")

except Exception as e:
    print("Error occurred:", e)