# SAMPLE DOB Violations Lookup (New)

## Purpose
To obtain DOB Violation data for building(s) within NYC. This references newer NYC DOB data. Use other endpoints to get older violations including BIS Violations. 

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/855j-jady/query.json`

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

### SAMPLE Body
```json
{
  "query": "SELECT * WHERE bin = '<bin>' AND device_type = 'Elevators'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

or

```json
{
  "query": "SELECT * WHERE device_number = '<device_number>' AND device_type = 'Elevators'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

or

```json
{
  "query": "SELECT * WHERE house_number = '<house_number>' AND upper(`street_name`) LIKE '%<street_name>%' AND device_type = 'Elevators'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```


### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `violation_number` = DOB Violation number given by the user
- `bin` = BIN (building identification number) given by the user
- `violation_status` = OPTIONS: "Active", "Dismissed", "Disputed Successfully", "Paid - Pending Dismissal", "Pending Dismissal", "Waived - Pending Dismissal"
- `boro` = NYC Borough. Options: "Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island"
- `house_number` | House Number, Building Number | text | Not the same as BIN, part of an address. May contain a hyphen. See sample cURL with query by address
- `street` | Street Name, Street | text | Part of address, see sample cURL with query by address
- `device_number` = Device number of the elevator given by the user
- `device_type` = Default is "Elevators"
- `violation_type` = Options: "ACC1", "ACJ1", "B", "DQ-EN-BENCH", "E", "EACJ1", "EJVIOS", "EVCAT1", "EVCAT5", "FISP", "FISPFCS", "FISPHAZ", "FISPNRF", "FTC-AEU-HAZ", "FTC-BE-EXT-HP", "FTC-BE-EXT-LP", "FTC-BE-INT-HP", "FTC-FC-SWARMP", "FTC-FC-UNSAFE", "FTC-PS-UNSAFE", "FTC-VT-CAT1-CO", "FTC-VT-CAT1-HA", "FTC-VT-CAT1-NJ", "FTC-VT-PER-CO", "FTC-VT-PER-HA", "FTF-EL-ENRF", "FTF-EL-PHOTOL", "FTF-EN-BENCH", "FTF-EN-EARCX", "FTF-EN-LL97320", "FTF-EN-LL97321", "FTF-PL-PER", "FTF-PS-INITL", "FTF-PS-INITL-PE", "FTF-RW-INITL", "FTF-SC-INITL", "FTF-SP-FINAL", "FTF-VT-CAT1-CO", "FTF-VT-CAT1-HA", "FTF-VT-CAT1-NJ", "FTF-VT-PER-CO", "FTF-VT-PER-HA", "FTF-VT-PER-NJ", "FTP-EN-EGRDEA", "FTX-EN-LL97320", "HBLVIO", "HVCAT5", "JVCAT5", "JVIOS", "L1198", "LBLVIO", "LL1081", "LL10/81", "LL1198", "LL11/98", "LL6291", "VCAT1"
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted

## Sample cURL (with real BIN, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/855j-jady/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE device_number = '\''1P28882'\'' AND device_type = '\''Elevators'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": "10"
  }
}'
```

### Sample Response (from sample cURL above)
```json
[
  {
    "bin": "1012699",
    "violation_issue_date": "2025-08-29T00:00:00.000",
    "violation_number": "VIO-FTF-VT-PER-202412-0001266",
    "violation_type": "FTF-VT-PER-CO",
    "violation_remarks": "Violation Issued-Failure To File 2024 Periodic Inspection Report",
    "violation_status": "Active",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2024-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-cw5w.fwj6_qjzx",
    ":version": "rv-awab~425a.vpwh",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2024-09-11T00:00:00.000",
    "violation_number": "VIO-FTF-VT-CAT1-202312-0001041",
    "violation_type": "FTF-VT-CAT1-CO",
    "violation_remarks": "Violation Issued-Failure To File 2023 Cat1 Test Report",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2023-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-uba3_wysf~fjdg",
    ":version": "rv-cvzp-x9mg_ujm3",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2024-09-11T00:00:00.000",
    "violation_number": "VIO-FTF-VT-PER-202312-0001416",
    "violation_type": "FTF-VT-PER-CO",
    "violation_remarks": "Violation Issued-Failure To File 2023 Periodic Inspection Report",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2023-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-va3y.zxd4_jshm",
    ":version": "rv-yd74-5qps_vqzv",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2023-10-23T00:00:00.000",
    "violation_number": "VIO-FTC-VT-CAT1-202012-0007901",
    "violation_type": "FTC-VT-CAT1-CO",
    "violation_remarks": "Violation Issued-Failure To File 2020 Cat1 Test Affirmation of Correction",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2020-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-cssn-45u2-2fu2",
    ":version": "rv-nxfd.vkh6_mmev",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2023-10-23T00:00:00.000",
    "violation_number": "VIO-FTC-VT-CAT1-202212-0015129",
    "violation_type": "FTC-VT-CAT1-CO",
    "violation_remarks": "Violation Issued-Failure To File 2022 Cat1 Test Affirmation of Correction",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2022-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-u36t_ejmy.mjr9",
    ":version": "rv-furu.5ysh-dhb7",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2016-11-14T00:00:00.000",
    "violation_number": "111416ACC101015",
    "violation_type": "ACC1",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2014-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-i6gy-rau8_fah3",
    ":version": "rv-a3yx_fuag_b95e",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2014-10-31T00:00:00.000",
    "violation_number": "103114EVCAT100421",
    "violation_type": "EVCAT1",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2013-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-35kt.9kj9_cbhc",
    ":version": "rv-8fpd~bmer-fxy4",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2014-03-31T00:00:00.000",
    "violation_number": "033114EVCAT100664",
    "violation_type": "EVCAT1",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2012-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-efuu-nfcv.c8zm",
    ":version": "rv-i26x.rrgr-i8er",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2012-10-01T00:00:00.000",
    "violation_number": "100112EVCAT100540",
    "violation_type": "EVCAT1",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2011-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-qssk.c4bv_qe9u",
    ":version": "rv-szm9.6d22_ufdy",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  },
  {
    "bin": "1012699",
    "violation_issue_date": "2011-12-13T00:00:00.000",
    "violation_number": "121311EVCAT100515",
    "violation_type": "EVCAT1",
    "violation_status": "Dismissed",
    "device_number": "1P28882",
    "device_type": "Elevators",
    "cycle_end_date": "2010-12-31T00:00:00.000",
    "borough": "Manhattan",
    "block": "720",
    "lot": "55",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "city": "New York",
    "state": "New York",
    "zip": "10011",
    "latitude": "40.746803",
    "longitude": "-74.002082",
    "community_board": "104",
    "council_district": "3",
    "bbl": "1007200055",
    "census_tract_2020_": "93",
    "neighborhood_tabulation_area_nta_2020_": "Chelsea-Hudson Yards",
    ":id": "row-qjv8~jv5s~nmft",
    ":version": "rv-h658.i4zj.awbn",
    ":created_at": "2026-01-20T19:49:08.065Z",
    ":updated_at": "2026-01-20T19:49:08.065Z"
  }
]
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/855j-jady`

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
results = client.get("855j-jady", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```