import requests
import json

# Send GET request to SpaceX API endpoint for upcoming launches
response = requests.get("https://api.spacexdata.com/v4/launches/upcoming")

# Parse JSON response
launches = json.loads(response.text)

# Loop through launches and print relevant information
for launch in launches:
    print("Flight Number:", launch["flight_number"])
    print("Mission Name:", launch["name"])
    print("Launch Date and Time:", launch["date_utc"])
    print("Launch Site:", launch["launchpad"])
    print()
