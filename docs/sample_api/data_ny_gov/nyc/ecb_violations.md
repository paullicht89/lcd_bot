# SAMPLE ECB Violation Lookup

## Purpose
To lookup ECB violations for building(s) within NYC.

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/6bgk-3dad/query.json`

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
  "query": "SELECT * WHERE bin = '<bin>'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

or

```json
{
  "query": "SELECT * WHERE ecb_violation_number = '<ecb_no>'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `ecb_no` = ECB Violation number given by the user
- `bin` = BIN (building identification number) given by the user
- `ecb_violation_status` = Status of the violation. Options: 'ACTIVE', 'RESOLVE', 'Unknown'
- `hearing_status` = Status of the ECB Hearing. Options: "ADMIN/IN-VIO", "CURED/IN-VIO", "DEFAULT", "IN VIOLATION", "PENDING", "POP/IN-VIO", "STIPULATION/IN-VIO", "WRITTEN OFF"
- `severity` = The severity class of the violation. Options: "CLASS-1", "CLASS-2", "CLASS-3", "Hazardous", "Non-Hazardous", "Unknown"
- `violation_type` = Default is "Elevators"
- `certification_status` = Status of the correction filing. Options: "CERTIFICATE ACCEPTED", "CERTIFICATE DISAPPROVED", "CERTIFICATE PENDING", "COMPLIANCE-INSP/DOC", "CURE ACCEPTED", "N/A - DISMISSED", "NO COMPLIANCE RECORDED", "REINSPECTION SHOWS STILL IN VIOLATION", "REINSPECTION SHOWS VIOLATION GOOD"
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted

## Sample cURL (with real BIN, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/6bgk-3dad/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE bin = '\''1012699'\'' AND violation_type = '\''Elevators'\''",
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
    "isn_dob_bis_extract": "36731",
    "ecb_violation_number": "38013194R",
    "ecb_violation_status": "RESOLVE",
    "dob_violation_number": "061391E1426A1",
    "bin": "1012699",
    "boro": "1",
    "block": "00720",
    "lot": "00055",
    "hearing_date": "19911212",
    "hearing_time": "1030",
    "served_date": "19910815",
    "issue_date": "19910613",
    "severity": "Non-Hazardous",
    "violation_type": "Elevators",
    "respondent_name": "418 RENROV INC",
    "respondent_house_number": "416",
    "respondent_street": "WEST   23 STREET",
    "respondent_city": "NY",
    "respondent_zip": "10011",
    "violation_description": "28L,20L,8J,60M,74M,(60)PROVIDE CWT BUFFER (74)PROVIDE FAN GUARD",
    "penality_imposed": "0",
    "amount_paid": "0",
    "balance_due": "0",
    "infraction_code1": "B8G",
    "section_law_description1": "27-127                                                                      FAILURE TO MAINTAIN ELEVATOR",
    "hearing_status": "DISMISSED",
    "certification_status": "N/A - DISMISSED",
    ":id": "row-q8y7-45uz.3sk7",
    ":version": "rv-jmac.vws9.z5jj",
    ":created_at": "2025-03-03T14:31:52.675Z",
    ":updated_at": "2025-03-03T14:31:52.675Z"
  },
  {
    "isn_dob_bis_extract": "260131",
    "ecb_violation_number": "38093120R",
    "ecb_violation_status": "RESOLVE",
    "dob_violation_number": "010600A1300A1",
    "bin": "1012699",
    "boro": "1",
    "block": "00720",
    "lot": "00055",
    "hearing_date": "20000224",
    "hearing_time": "1030",
    "served_date": "20000106",
    "issue_date": "20000106",
    "severity": "Non-Hazardous",
    "violation_type": "Elevators",
    "respondent_name": "TEMPO MANAGERS",
    "respondent_house_number": "416",
    "respondent_street": "WEST   23 STREET",
    "respondent_city": "NY",
    "respondent_zip": "10011",
    "violation_description": "47A,47O.",
    "penality_imposed": "0",
    "amount_paid": "0",
    "balance_due": "0",
    "infraction_code1": "BP7",
    "section_law_description1": "27-987                                                                      FAILURE TO MAINTAIN ELEVATOR",
    "hearing_status": "CURED/IN-VIO",
    "certification_status": "CURE ACCEPTED",
    ":id": "row-i4zb~i442_edn8",
    ":version": "rv-97pr-cf3t.7eap",
    ":created_at": "2025-03-03T14:31:52.675Z",
    ":updated_at": "2025-03-03T14:31:52.675Z"
  },
  {
    "isn_dob_bis_extract": "438938",
    "ecb_violation_number": "38152330M",
    "ecb_violation_status": "RESOLVE",
    "dob_violation_number": "042105E1225A1",
    "bin": "1012699",
    "boro": "1",
    "block": "00720",
    "lot": "00055",
    "hearing_date": "20050609",
    "hearing_time": "1030",
    "served_date": "20050421",
    "issue_date": "20050421",
    "severity": "Non-Hazardous",
    "violation_type": "Elevators",
    "respondent_name": "TEMPO MANAGERS",
    "respondent_house_number": "416",
    "respondent_street": "WEST   23 STREET",
    "respondent_city": "NY",
    "respondent_zip": "10011",
    "violation_description": "08V01/17M11/17D06/23I11/25W06/40J01/52O11/55O02/64I10/66O02/69K10.17M11 REPLACE ONE GIB MISISNG AT BASEMENT HALL DOOR.17D16 SECURE ONE GIB ON 4TH FLOOR.23I11 REPLACE DAMAGED HALL BUTOTN IN BASEMENT.40J01 ADJUST",
    "penality_imposed": "0",
    "amount_paid": "0",
    "balance_due": "0",
    "infraction_code1": "BP7",
    "section_law_description1": "27-987                                                                      FAILURE TO MAINTAIN ELEVATOR",
    "hearing_status": "CURED/IN-VIO",
    "certification_status": "CURE ACCEPTED",
    ":id": "row-gj9y_9uxa-mk28",
    ":version": "rv-ujud_a454~9r4r",
    ":created_at": "2025-03-03T14:31:52.675Z",
    ":updated_at": "2025-03-03T14:31:52.675Z"
  },
  {
    "isn_dob_bis_extract": "1644575",
    "ecb_violation_number": "39029310H",
    "ecb_violation_status": "RESOLVE",
    "bin": "1012699",
    "boro": "1",
    "block": "00720",
    "lot": "0055",
    "hearing_date": "20210415",
    "hearing_time": "830",
    "served_date": "20200925",
    "issue_date": "20200925",
    "severity": "CLASS - 1",
    "violation_type": "Elevators",
    "respondent_name": "416 W 23RD STREET PARTNER",
    "respondent_house_number": "243",
    "respondent_street": "5 AVENUE",
    "respondent_city": "NEW YORK",
    "respondent_zip": "10016",
    "violation_description": "CLASS 1 CAR CEASE USE CAR DOOR RESTRICTOR IS NOT WORKING MISSING PARTS REPAIR ,BRAKE TAG EXPIRED PROVIDE FIRE EXTINGUISHER TAG EXPIRED PROVIDE.",
    "penality_imposed": "1250",
    "amount_paid": "1250",
    "balance_due": "0",
    "infraction_code1": "151",
    "section_law_description1": "28-301.1                                                                    FAILURE TO MAINTAIN BUILDING IN CODE COMPLIANT MANNER: SERVICE EQUIPME",
    "aggravated_level": "NO",
    "hearing_status": "IN VIOLATION",
    "certification_status": "CERTIFICATE ACCEPTED",
    ":id": "row-4vrv-gthn_dwjt",
    ":version": "rv-vpaj_8thb.p4pa",
    ":created_at": "2025-10-20T17:02:25.556Z",
    ":updated_at": "2025-10-20T17:02:25.556Z"
  },
  {
    "isn_dob_bis_extract": "1662941",
    "ecb_violation_number": "39175026X",
    "ecb_violation_status": "RESOLVE",
    "bin": "1012699",
    "boro": "1",
    "block": "00720",
    "lot": "0055",
    "hearing_date": "20261201",
    "hearing_time": "830",
    "served_date": "20260127",
    "issue_date": "20260127",
    "severity": "CLASS - 1",
    "violation_type": "Elevators",
    "respondent_name": "GW 416 WEST 23RD STREET L",
    "respondent_street": "550AMERICAN AVE STE 1",
    "respondent_city": "KING OF PRUSSIA",
    "respondent_zip": "19406",
    "violation_description": "5/L/10 CAR CEASE USE CLASS 1 CAR DOOR RESTRICTOR DEFECTIVE REPAIR,70/L/10 PIT LIGHT DEFECTIVE REPAIR, 70/Z/2 WATER IN PIT CLEAN.",
    "penality_imposed": "1250",
    "amount_paid": "0",
    "balance_due": "1250",
    "infraction_code1": "151",
    "section_law_description1": "28-301.1                                                                    FAILURE TO MAINTAIN BUILDING IN CODE COMPLIANT MANNER: SERVICE EQUIPME",
    "aggravated_level": "NO",
    "certification_status": "CERTIFICATE ACCEPTED",
    ":id": "row-gkwd-tzti~8rvr",
    ":version": "rv-ydpi~3gtz_hkgk",
    ":created_at": "2026-05-08T17:00:03.284Z",
    ":updated_at": "2026-05-08T17:00:03.284Z"
  }
]
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/6bgk-3dad`

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
results = client.get("6bgk-3dad", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```