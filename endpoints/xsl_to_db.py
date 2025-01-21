import os
import pandas as pd
from db import db  # Import your DB class

def parse_and_upload_to_db(file_path, program, predmet):
    """Parse the Excel file and upload data to the database."""
    try:
        # Read Excel file and skip the first 3 rows
        df = pd.read_excel(file_path, skiprows=3, engine='xlrd', usecols="C,D,E,F,H,J",
                           names=['datum', 'ura', 'prostor', 'izvajanje', 'skupina', 'izvajalec'])

        print("File read successfully.")

        # Convert times and dates
        start_times = df['ura'].str.split('-', expand=True)[0]
        end_times = df['ura'].str.split('-', expand=True)[1]

        # Prepare the entries for MongoDB
        entries = []
        for _, row in df.iterrows():
            entry = {
                'Dan': pd.to_datetime(row['datum'], format='%d.%m.%Y').day_name(locale='sl_SI'),
                'Datum': row['datum'],
                'Ura': row['ura'],
                'Prostor': row['prostor'],
                'Izvajanje': row['izvajanje'],
                'Skupina': row['skupina'],
                'Izvajalec': row['izvajalec']
            }
            entries.append(entry)

        # Create the document structure
        db_entry = {
            "program": program,
            "predmet": predmet,
            "entries": entries
        }

        # Upload to MongoDB
        db.schedules.update_one(
            {"program": program, "predmet": predmet},
            {"$set": db_entry},
            upsert=True
        )

        print(f"Data for program '{program}' and predmet '{predmet}' uploaded successfully.")

    except Exception as e:
        print(f"Error processing file: {e}")


def main():
    # Define download directory
    download_dir = os.path.abspath("./downloads")
    files = os.listdir(download_dir)

    # List available files
    print("\nAvailable Files:")
    for index, file in enumerate(files):
        print(f"{index + 1}. {file}")

    # Prompt the user to select an index
    while True:
        try:
            target_index = int(input("\nEnter the number corresponding to your desired option: ")) - 1
            if 0 <= target_index < len(files):
                break
            else:
                print(f"Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get the selected file path
    file_path = os.path.join(download_dir, files[target_index])

    # Prompt for program and predmet
    program = input("Enter the program name: ")
    predmet = input("Enter the predmet name: ")

    # Parse and upload the selected file
    parse_and_upload_to_db(file_path, program, predmet)


if __name__ == "__main__":
    main()
