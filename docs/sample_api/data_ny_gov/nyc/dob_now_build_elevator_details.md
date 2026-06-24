# SAMPLE DOB NOW BUILD ELEVATOR DETAILS

## Purpose
To obtain elevator device details from DOB Now Build

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/juyv-2jek/query.json`

### Authorization
No Auth

### Headers
```json
{
    "content-type": "application/json",
    "x-app-token": "<app_token>"
}
```

### Available Parameters
No parameters

### Body (with most common query - device_number)
```json
{
  "query": "SELECT * WHERE device_number = '<device-number>'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

#### Fields to Query In the Body (relevant to this app)
FORMAT: field_name | friendly_name(s) | type | notes

- `device_id` OR `bis_nyc_device_id` | Device Number, Device No, Device, Elevator, etc. | text
- `job_filing_number` | Filing number of permit | text
- `device_type` | Type of Device | text | Default = "Elevator"
- `physical_address` | Address of the device | text | Use "upper(`physical_address`) LIKE '%part of address here%'"

### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted
- ALL potential fields to be queried above

## Sample cURL (with real device number, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/juyv-2jek/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE bis_nyc_device_id='\''1P28882'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": 1000
  }
}'
```

### Sample Response
```json
[
  {
    "job_filing_number": "M00148400-I1",
    "device_id": "1P28882",
    "device_type": "Elevator",
    "device_status": "Active",
    "bis_nyc_device_id": "1P28882",
    "elevator_type": "Passenger",
    "elevator_sub_type": "N/A",
    "physical_address": "416 WEST 23 STREET",
    "only_elevator_in_building": "Yes",
    "occupant_evacuation_elevator": "No",
    "meets_the_stretcher_car": "No",
    "device_confirming_with_seismic": "No",
    "fire_emergency_phase": "No",
    "destination_dispatch_system": "No",
    "fire_service_access_elevator": "No",
    "device_in_conjunction_with": "No",
    "new_hoistway": "No",
    "loft_law_building": "No",
    "device_job_description": "Install door lock monitoring system to meet NYC Code requirements.  All work to comply with  A17.3 o",
    "machine_manufacturer": "existing",
    "machine_model": "existing",
    "machine_type": "Traction",
    "type_of_machine_break": "Drum",
    "machine_location": "motor room @ roof",
    "controller_manufacturer": "Armor",
    "controller_model": "8Arm",
    "controller_location": "motor room @ roof",
    "powertype": "AC",
    "main_supply_power_type": "AC",
    "travel_from_floor": "B",
    "travel_to_floor": "6",
    "total_travel_feet": "60",
    "number_of_stops": "7",
    "elevator_capacity_lbs": "1,500",
    "elevator_speed_fpm": "100",
    "elevator_control": "Resistance",
    "mode_of_operation": "Automatic P.B.",
    "load_weighing_device": "No",
    "glass_hoistway": "No",
    "atruim_elevator": "No",
    "regenerative_drive": "No",
    "car_safety_type": "Instantaneous",
    "counter_weight_safety_type": "N/A",
    "car_opening": "Door",
    "car_opening_direction": "Horizontal",
    "car_opening_operation": "Power",
    "contact_type": "exisitng",
    "elevator_manufacturer": "exsiting",
    "car_to_counterweight_ratio": "40",
    "top_emergency_exit_min_area": "400",
    "top_emergency_exit_min_side": "16",
    "car_inside_width_feet": "5",
    "car_inside_width_inches": "2",
    "car_inside_depth_feet": "3",
    "car_inside_depth_inches": "6",
    "car_inside_area": "18.08",
    "sized_for_stretcher": "No",
    "glass_car": "No",
    "multicompartment": "No",
    "hoist_opening": "Door",
    "hoist_direction": "Horizontal",
    "elevator_operation": "Power",
    "elevator_doorfeatures": "Interlocks",
    "interlocks_type": "MO",
    "hoist_manufacturer": "GAL",
    "elevator_landing": "7",
    "number_of_openings_front": "7",
    "number_of_openings_side": "0",
    "number_of_openings_rear": "0",
    "total_number_of_openings": "7",
    "door_monitoring_circuits": "Yes",
    "fire_rated_construction_type": "Yes",
    "self_closing_emergency_doors": "No",
    "interlockin_blind_hoistway": "No",
    "car_buffer_type": "Spring",
    "car_buffer_manufacturer": "exisitng",
    "car_buffer_engagement_speed": "100",
    "car_buffer_stroke_feet": "0",
    "car_buffer_stroke_inches": "1.5",
    "car_buffer_reduced_stroke": "No",
    "counter_weight_buffer_type": "Spring",
    "counter_weight_buffer": "exisitng",
    "counter_weight_buffer_1": "100",
    "counter_weight_buffer_stroke": "0",
    "counter_weight_buffer_stroke_1": "1.5",
    "compensation_means": "N/A",
    "elevator_length_feet": "0",
    "elevator_length_inches": "0E-10",
    "counter_weight_buffer_reduced": "No",
    "occupied_space_below": "No",
    "compensation_tie_down": "No",
    "counter_weight_guard": "Yes",
    "plunger_type": "Single Plunger",
    ":id": "row-jvsz~j8xv~jwgq",
    ":version": "rv-rqu4.tqkt~8ud7",
    ":created_at": "2025-06-02T19:03:20.561Z",
    ":updated_at": "2025-06-02T19:03:20.561Z"
  }
]
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/juyv-2jek`

### Sample Python Pandas Code Snippet
```python
#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("juyv-2jek", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```