# SAMPLE DOB NOW SAFETY COMPLIANCE

## Purpose
To obtain most recent safety compliance data of elevator devices from NYC DOB Now including Category 1 (CAT1), Category 5 (CAT5), Periodic (PER), and other elevator inspections within New York City (NYC)

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/e5aq-a4j2/query.json`

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

- `device_number` | Device Number, Device No, Device, Elevator, etc. | text
- `periodic_report_year` | Periodic Report Year | text
- `cat1_report_year` | CAT1 Report Year | text
- `cat1_latest_report_filed` | CAT1 Latest Report Filed Date | floating_timestamp | format: YYYY-MM-DDTHH:mm:ss.#### (ex: "2014-10-13T00:00:00.000")
- `cat5_latest_report_filed` | CAT5 Latest Report Filed Date | floating_timestamp | format: YYYY-MM-DDTHH:mm:ss.#### (ex: "2014-10-13T00:00:00.000")
- `periodic_latest_inspection` | Periodic Latest Report Filed Date | floating_timestamp | format: YYYY-MM-DDTHH:mm:ss.#### (ex: "2014-10-13T00:00:00.000")
- `bin` | BIN, Building Identification Number | text
- `borough` | Borough, Boro | text
- `house_number` | House Number, Building Number | text | Not the same as BIN, part of an address. May contain a hyphen. See sample cURL with query by address
- `street_name` | Street Name, Street | text | Part of address, see sample cURL with query by address

### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted
- ALL potential fields to be queried above

## Sample cURL (with real device number, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/e5aq-a4j2/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ****' \
  --data '{
  "query": "SELECT * WHERE device_number = '\''1P29384'\''",
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
    "device_number": "1P29384",
    "device_type": "Elevator",
    "device_status": "Active",
    "status_date": "2022-02-15T00:00:00.000",
    "equipment_type": "ElectricElevators",
    "periodic_report_year": "2025",
    "cat1_report_year": "2025",
    "cat1_latest_report_filed": "2025-04-17T00:00:00.000",
    "cat5_latest_report_filed": "2022-03-29T00:00:00.000",
    "periodic_latest_inspection": "2025-08-14T00:00:00.000",
    "bin": "1079340",
    "borough": "MANHATTAN",
    "house_number": "345",
    "street_name": "EAST  101 STREET",
    "block": "1673",
    "lot": "6",
    "zip_code": "10029",
    "latitude": "40.787156",
    "longitude": "-73.944074",
    "communitydistrict": "111",
    "citycouncildistrict": "08",
    "bbl": "1016730006",
    "censustract": "164",
    "ntaname": "East Harlem (South)",
    ":id": "row-fm3e_d9d5.dpqu",
    ":version": "rv-cm5h.xkwu~i34n",
    ":created_at": "2026-01-26T21:32:03.312Z",
    ":updated_at": "2026-01-26T21:32:03.312Z"
  }
]
```

## Sample cURL by Address
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/e5aq-a4j2/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE house_number = '\''94-00'\'' AND upper(`street_name`) LIKE '\''%DITMARS%'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": 1000
  }
}'
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/e5aq-a4j2`

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
results = client.get("e5aq-a4j2", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```