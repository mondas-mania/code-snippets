import requests
import csv
import os

if os.environ.get("GOOGLE_API_KEY") == None:
    apikey = input("Please enter a Google Maps API Key: ")
else:
    apikey = os.environ["GOOGLE_API_KEY"]

import_path = input("Please enter a file path for the CSV to be imported: ") if os.environ.get("DISTANCE_INPUT_PATH") == None else os.environ["DISTANCE_INPUT_PATH"]
output_path = input("Please enter a file path for the output CSV to be created at: ") if os.environ.get("DISTANCE_OUTPUT_PATH") == None else os.environ["DISTANCE_OUTPUT_PATH"]
input_delimiter = "," if os.environ.get("DISTANCE_INPUT_DELIMITER") == None else os.environ["DISTANCE_INPUT_DELIMITER"]
output_delimiter = "," if os.environ.get("DISTANCE_OUTPUT_DELIMITER") == None else os.environ["DISTANCE_OUTPUT_DELIMITER"]

# Can be imperial, metric - for miles versus km respectively
units = "imperial" if os.environ.get("DISTANCE_UNITS") == None else os.environ["DISTANCE_UNITS"]
# Can be driving, walking, bicycling, transit. Defaults to driving.
mode = "driving" if os.environ.get("DISTANCE_MODE") == None else os.environ["DISTANCE_MODE"]

not_founds = 0

with open(import_path, newline='', encoding='utf-8-sig') as csvfile_in:
    with open(output_path, "w", newline='', encoding='utf-8-sig') as csvfile_out:
        csv_reader = csv.reader(csvfile_in, delimiter=input_delimiter)
        csv_writer = csv.writer(csvfile_out, delimiter=output_delimiter)
        csvfile_out.writelines([f"sep={output_delimiter}\n"])
        for i, row in enumerate(csv_reader):
            if i % 100 == 0:
                print(f"Processing row {i}")
            
            if row[0] == f"sep=":
                continue

            origin = row[0]
            destination = row[1]
            try:
                url = f"https://maps.googleapis.com/maps/api/directions/json?origin='{origin}'&destination='{destination}'&key={apikey}&mode={mode}&units={units}"
                r = requests.get(url)
                json_out = r.json()
                if json_out["status"] == "NOT_FOUND":
                    csv_writer.writerow([origin, destination, "NOT_FOUND"])
                    not_founds += 1
                    continue
                else:
                    meters_value = json_out["routes"][0]["legs"][0]["distance"]["value"]
                    output_value = meters_value * 0.000621 if units == "imperial" else meters_value / 1000
                    csv_writer.writerow([origin, destination, f"{output_value:.2f}"])
            except Exception as e:
                print(f"{e} at line {i}")

print(f"Execution finished with {not_founds} NOT_FOUNDs.")