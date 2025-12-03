import json

# Read the trips.json file
with open('trips.json', 'r') as file:
    trips = json.load(file)

# Print some values from each trip
for trip in trips:
    print(f"Trip ID: {trip['trip_id']}")
    print(f"Name: {trip['trip_name']}")
    print(f"Location: {trip['trip_location']}")
    print(f"Price: ${trip['trip_price']}")
    print(f"Date: {trip['trip_start_date']} to {trip['trip_end_date']}")
    print(f"Status: {trip['trip_status']}")
    print("-" * 50)

