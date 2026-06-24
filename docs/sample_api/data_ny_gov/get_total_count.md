# SAMPLE GET TOTAL COUNT FROM API CALL

## Purpose
To obtain total number of records from an api call to determine the pageSize and pageNumber(s) needed in the body. This should be run prior to any call to ensure all results are found and to determine if the API call must be run multiple times for multiple pageNumber(s) and/or pageSize(s).

NOTE: if using the default pageSize: 1000, any total 1000 and under should not require additional calls.

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/e5aq-a4j2/query.json`

NOTE: this will work with any call

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
  "query": "query": "SELECT count(*) AS total WHERE <remaining query here>",
  "page": { "pageNumber": 1, "pageSize": 1 }
}
```

#### Fields to Query In the Body (relevant to this app)
SEE RELEVANT API CALL

### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted
- ALL potential fields to be queried above

## Sample cURL (get count of ECB violations for a specific building, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/6bgk-3dad/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: nA1dCwhk05fsdEWYM0umh84sH' \
  --data '{
  "query": "SELECT count(*) AS total WHERE bin = '\''1012699'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": 1
  }
}'
```

### Sample Response
```json
[
  {
    "total": "30"
  }
]
```

#### Meaning of sample response
From this response, if using the following in the body for an actual API call `"page": { "pageNumber": 1, "pageSize": 10 }`, since the total count is 30, you must repeat the call 3 times with pageNumber 1, 2, and 3 OR use `"page": { "pageNumber": 1, "pageSize": 30 }` or even `"page": { "pageNumber": 1, "pageSize": 1000 }`.



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