# SAMPLE OATH Hearings Lookup

## Purpose
To lookup OATH Hearing Details for ECB Violations

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/jz4z-kudi/query.json`

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

### Body
```json
{
  "query": "SELECT * WHERE ticket_number='039175026X'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```


### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `ticket_number` = ECB violation number with a 0 in the front
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted

## Sample cURL (app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/jz4z-kudi/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE ticket_number='\''039175026X'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": 1000
  }
}'
```

### Sample Response (from sample cURL above)
```json
[
  {
    "ticket_number": "039175026X",
    "violation_date": "2026-01-27T00:00:00.000",
    "violation_time": "10:08:00",
    "issuing_agency": "DEPT. OF BUILDINGS",
    "respondent_last_name": "GW 416 WEST 23RD STREET LLC A",
    "balance_due": "1250",
    "violation_location_borough": "MANHATTAN",
    "violation_location_block_no": "00720",
    "violation_location_lot_no": "0055",
    "violation_location_house": "416",
    "violation_location_street_name": "WEST 23 STREET",
    "violation_location_city": "NEW YORK",
    "violation_location_zip_code": "10011",
    "violation_location_state_name": "NEW YORK",
    "respondent_address_borough": "NOT NYC",
    "respondent_address_zip_code": "19406",
    "hearing_status": "RESCHEDULED",
    "hearing_result": "ADJOURNED",
    "scheduled_hearing_location": "BY PHONE T",
    "hearing_date": "2026-12-01T00:00:00.000",
    "hearing_time": "08:30:00",
    "total_violation_amount": "1250",
    "violation_details": "5 L 10 CAR CEASE USE CLASS 1 CAR DOOR RESTRICTOR DEFECTIVE REPAIR,70 L10 PIT LIGHT DEFECTIVE REPAIR, 70 Z 2 WATER IN PIT CLEAN.",
    "penalty_imposed": "1250",
    "paid_amount": "0",
    "additional_penalties_or_late_fees": "0",
    "compliance_status": "Penalty Due",
    "charge_1_code": "B151",
    "charge_1_code_section": "28-304",
    "charge_1_code_description": "FAILURE TO MAINTAIN ELEVATOR OR CONVEYING SYSTEM",
    "charge_1_infraction_amount": "1250",
    ":id": "row-jt29_d48m.p5nq",
    ":version": "rv-utf8~dxpe-qn4g",
    ":created_at": "2026-01-30T02:16:13.243Z",
    ":updated_at": "2026-05-21T01:37:50.781Z"
  }
]
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/jz4z-kudi`

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
results = client.get("jz4z-kudi", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```