# SAMPLE NYS LICENSE LOOKUP

## Purpose
To lookup individual AND business elevator license details from NYS

## URI:

### Individual Lookup
- Type: = `POST`
- Base URL = `https://data.ny.gov/api/v3/views/cxfs-ya8e/query.json`

### Business Lookup
- Type: = `POST`
- Base URL = `https://data.ny.gov/api/v3/views/jrac-r9vc/query.json`

#### Authorization
No Auth

#### Headers
```json
{
    "content-type": "application/json",
    "x-app-token": "<app_token>"
}
```

#### Available Parameters
No parameters

#### Sample Body - Individual (with most common query - last_name)
```json
{
  "query": "SELECT * WHERE upper(`last_name`) LIKE '%UPPERCASE_LAST_NAME%'",
  "page": { "pageNumber": 1, "pageSize": "1000" },
  "includeSynthetic": false
}
```

#### Sample Body - Business (with most common query - business_name)
```json
{
  "query": "SELECT * WHERE upper(`business_name`) LIKE '%UPPERCASE_BUSINESS_NAME%'",
  "page": { "pageNumber": 1, "pageSize": "1000" },
  "includeSynthetic": false
}
```

#### Fields to Query In the Body (relevant to this app)
FORMAT: field_name | friendly_name(s) | type | notes

- `license_number` | License Number | text
- `license_type` | License Type | text
- `business_name` | Business Name | text | Business Search Only
- `city` | City of the business | text | Business Search Only
- `zip_code` | ZIP code of the business | text | Business Search Only
- `first_name` | First name of the licensee | text | Individual Search Only
- `last_name` | Last name of the licensee | text | Individual Search Only

### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted
- ALL potential fields to be queried above

## Sample cURL (Individual)
```cURL
curl --request POST \
  --url https://data.ny.gov/api/v3/views/cxfs-ya8e/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE upper(`last_name`) LIKE '\''%LICHT%'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": "1000"
  },
  "includeSynthetic": false
}'
```

### Sample Response
```json
[
  {
    "license_number": "23-6LIFR-SHEL",
    "license_type": "Elevator Inspector License (SH132)",
    "first_name": "Richard",
    "last_name": "Licht",
    "issued_date": "2023-11-19T00:00:00.000",
    "expiration_date": "2025-12-31T00:00:00.000",
    "license_status": "Expired"
  },
  {
    "license_number": "23-6LIY7-SHEL",
    "license_type": "Elevator Mechanic License (SH132)",
    "first_name": "Richard",
    "last_name": "Licht",
    "issued_date": "2023-11-18T00:00:00.000",
    "expiration_date": "2025-12-31T00:00:00.000",
    "license_status": "Expired"
  },
  {
    "license_number": "25-61V9U-SHEL",
    "license_type": "Elevator Mechanic License (SH132)",
    "first_name": "Carl",
    "last_name": "Licht",
    "issued_date": "2025-12-04T00:00:00.000",
    "expiration_date": "2027-12-31T00:00:00.000",
    "license_status": "Active"
  },
  {
    "license_number": "23-6LDII-SHEL",
    "license_type": "Elevator Mechanic License (SH132)",
    "first_name": "Joseph",
    "last_name": "Lichtman",
    "issued_date": "2023-10-21T00:00:00.000",
    "expiration_date": "2025-12-31T00:00:00.000",
    "license_status": "Expired"
  }
]
```

### API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/cxfs-ya8e`

#### Sample Python Pandas Code Snippet
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
results = client.get("cxfs-ya8e", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```

## Sample cURL (Individual)
```cURL
curl --request POST \
  --url https://data.ny.gov/api/v3/views/jrac-r9vc/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE upper(`business_name`) LIKE '\''%LCD%'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": "1000"
  },
  "includeSynthetic": false
}'
```

### Sample Response
```json
[
  {
    "license_number": "26-6LIH1-SHEL",
    "license_type": "Elevator Inspection Contractor License (SH131)",
    "business_name": "LCD Elevator Repair Inc",
    "address": "224 East 2nd Street",
    "address_2": "Suite 200",
    "city": "Mineola",
    "state": "NY",
    "zip_code": "11501",
    "phone": "5167058817",
    "issued_date": "2026-02-13T00:00:00.000",
    "expiration_date": "2027-12-31T00:00:00.000",
    "license_status": "Active"
  },
  {
    "license_number": "26-6LIHP-SHEL",
    "license_type": "Elevator Contractor License (SH131)",
    "business_name": "LCD Elevator Repair Inc",
    "address": "224 East 2nd Street",
    "address_2": "Suite 200",
    "city": "Mineola",
    "state": "NY",
    "zip_code": "11501",
    "phone": "5167058817",
    "issued_date": "2026-02-13T00:00:00.000",
    "expiration_date": "2027-12-31T00:00:00.000",
    "license_status": "Active"
  }
]
```

### API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/jrac-r9vc`

#### Sample Python Pandas Code Snippet
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
results = client.get("jrac-r9vc", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```