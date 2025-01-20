# Distance between two locations using Google Maps API
This snippet will take a CSV input of source and destination locations in plain text and will output a CSV with that same data, plus the distance between them.

The API Documentation for the main request is found [here](https://developers.google.com/maps/documentation/directions/get-directions).

## Pre-Requisites
- The user must have the `requests` package installed in Python. This can be done via:
  ```
  pip install -r requirements.txt
  ```
  - N.B. `pip` may need to be substituted for `pip3`, `python -m pip` or `python3 -m pip` depending on your Python install.
- The user must have a [Google Maps API key](https://developers.google.com/maps/documentation/directions/get-api-key) that they are ready to use.
  - Note: This can incur billing in non-free trial accounts and at large-scale usage.
  - This can be set with the `GOOGLE_API_KEY` environment variable, otherwise it will be provided via text input upon running the script.
- The following other environment variables can be set:
  - `DISTANCE_INPUT_PATH` - The input filepath for the CSV. Will be prompted for input if not provided.
  - `DISTANCE_OUTPUT_PATH` - The output filepath for the CSV. Will be prompted for input if not provided.
  - `DISTANCE_INPUT_DELIMITER` - The delimiter for the input CSV. Will default to `,`.
  - `DISTANCE_OUTPUT_DELIMITER` - The delimiter for the output CSV. Will default to `,`.
  - `DISTANCE_UNITS` - The units for the output distances. Defaults to `imperial` to give values in Miles, otherwise `metric` to give values in Kilometers.
  - `DISTANCE_MODE` - The mode of travel for the output distance. Defaults to `driving`, with other valid values being `walking`, `bicycling` and `transit`.

## Possible optimisations
- Store a map of existing source-destination keys against distance values, to avoid re-querying the exact same journey. May save a large amount of requests to the API, at the cost of very little (relative) local memory.
- Refactor into function(s).
- Actual error handling, such as a Too Many Requests from Google.
- Closing both files if the script is cancelled. Currently none of the output data saves if the script finishes early due to user input (i.e. Ctrl+x). Proper error handling (as above) may allow the files to be closed gracefully.
- Investigate the newer [Routes API](https://developers.google.com/maps/documentation/routes).