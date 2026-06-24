# SAMPLE DOB Violations Lookup (Old)

## Purpose
To obtain DOB Violation data for building(s) within NYC. This references older NYC DOB BIS data. Use other endpoints to get newer violations including newer ECB Violations. 

## URI: 
- Type: = `POST`
- Base URL = `https://data.cityofnewyork.us/api/v3/views/3h2n-5cm9/query.json`

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
  "query": "SELECT * WHERE bin = '<bin>' AND violation_type_code = 'E'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

or

```json
{
  "query": "SELECT * WHERE device_number = '<device_number>' AND violation_type_code = 'E'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```

or

```json
{
  "query": "SELECT * WHERE house_number = '<house_number>' AND upper(`street_name`) LIKE '%<street_name>%' AND violation_type_code = 'E'",
  "page": { "pageNumber": 1, "pageSize": 1000 }
}
```


### Variables
- `app_token` = .env > NYS_APP_TOKEN
- `violation_number` = DOB Violation number given by the user (partial number, ex "9027/560099")
- `number` = FULL violation number given by the user (ex: "V*011216E9027/560099")
- `ecb_number` = ECB Violation number given by the user
- `bin` = BIN (building identification number) given by the user
- `boro` = NYC Borough. Options: "1", "2", "3", "4", "5". (1 = Manhattan, 2 = Bronx, 3 = Brooklyn, 4 = Queens, 5 = Staten Island)
- `violation_type_code` = Type of violation. Default is "E"
- `house_number` | House Number, Building Number | text | Not the same as BIN, part of an address. May contain a hyphen. See sample cURL with query by address
- `street_name` | Street Name, Street | text | Part of address, see sample cURL with query by address
- `device_number` = Device number of the elevator given by the user
- `violation_category` = Options:
- `pageNumber` = default is 1 can be adjusted
- `pageSize` = default is 1000 can be adjusted

## Sample cURL (with real BIN, app token blanked out)
```cURL
curl --request POST \
  --url https://data.cityofnewyork.us/api/v3/views/3h2n-5cm9/query.json \
  --header 'content-type: application/json' \
  --header 'x-app-token: ***' \
  --data '{
  "query": "SELECT * WHERE bin = '\''1012699'\'' AND violation_type_code = '\''E'\''",
  "page": {
    "pageNumber": 1,
    "pageSize": "1000"
  }
}'
```

### Sample Response (from sample cURL above)
```json
[
  {
    "isn_dob_bis_viol": "4831",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "19880812",
    "violation_type_code": "E",
    "violation_number": "11334/3",
    "house_number": "416",
    "street": "W 23 ST",
    "disposition_date": "19910613",
    "device_number": "1P28882",
    "description": "(27) MOUNT COUNTERWEIGHT & BUFFER (38) COVER DOOR OPERATOR                      (51) SECURE SMOKE HOLE GRATING (31) BASE MENT LEVELING",
    "number": "V*081288E11334/3",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-pux7.2d9r~s2k7",
    ":version": "rv-qdmq.jynv~8e5f",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "496437",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "19970618",
    "violation_type_code": "E",
    "violation_number": "1267A04",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "ecb_number": "38060982J",
    "number": "V061897E1267A04",
    "violation_category": "V-DOB VIOLATION - ACTIVE",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-9fse-fdyz.8kyp",
    ":version": "rv-jwp5_7qvq~8zh6",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "672291",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "19991027",
    "violation_type_code": "E",
    "violation_number": "9013/113589",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20130731",
    "disposition_comments": "PVT: RESOLVED BY SATISFACTORY CAT 1 INSPECTION",
    "description": "1P28882",
    "number": "V*102799E9013/113589",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-i3j4~bsxd-5prc",
    ":version": "rv-ww36_ss9e-ruj7",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "73103",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20020125",
    "violation_type_code": "E",
    "violation_number": "9444/147372",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20130731",
    "disposition_comments": "PVT: RESOLVED BY SATISFACTORY CAT 1 INSPECTION",
    "description": "1P28882",
    "number": "V*012502E9444/147372",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-ufjc~tccg.dikx",
    ":version": "rv-f5mh.4qfh-ifh3",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "887622",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20030318",
    "violation_type_code": "E",
    "violation_number": "9444/169065",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20130731",
    "disposition_comments": "PVT: RESOLVED BY SATISFACTORY CAT 1 INSPECTION",
    "description": "1P28882",
    "number": "V*031803E9444/169065",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-w3ga_66ay~et8n",
    ":version": "rv-arym-cfc4~n4d8",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "946734",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20031218",
    "violation_type_code": "E",
    "violation_number": "9013/188647",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_comments": "DELETED BY MTH ON 12/31/2003 BECAUSE DEVICE # MISSING",
    "number": "V121803E9013/188647",
    "violation_category": "V-DOB VIOLATION - ACTIVE",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-muzx_j4gm~hxs3",
    ":version": "rv-5p9q-vb5g.t865",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "946812",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20031218",
    "violation_type_code": "E",
    "violation_number": "9013/188647",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20130731",
    "disposition_comments": "PVT: RESOLVED BY SATISFACTORY CAT 1 INSPECTION",
    "device_number": "01P28882",
    "number": "V*121803E9013/188647",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-xxmn-exw4~qfs6",
    ":version": "rv-5kdt-mzwt_9m4g",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1012249",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20041201",
    "violation_type_code": "E",
    "violation_number": "9444/114638",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20050421",
    "disposition_comments": "AS PER INSPECTOR'S ROUTE SHEET",
    "device_number": "01P28882",
    "number": "V*120104E9444/114638",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-ypv7_d78y~b8pk",
    ":version": "rv-twic.uavk~m7gi",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1080080",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20050825",
    "violation_type_code": "E",
    "violation_number": "94441139937",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20070821",
    "disposition_comments": "PPN203 2YR TEST PERFORMED 7/17/07 BY NEW YORK ELEVATOR & ELECTRICAL COMPANY CERT",
    "device_number": "01P28882",
    "number": "V*082505E94441139937",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-hb6g.b6x6-tcqi",
    ":version": "rv-dskz.57kt-4y2m",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1209501",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "0055",
    "issue_date": "20070315",
    "violation_type_code": "E",
    "violation_number": "94441192588",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20070821",
    "disposition_comments": "PPN203 2YR TEST PERFORMED 7/17/07 BY NEW YORK ELEVATOR & ELECTRICAL COMPANY CERT",
    "device_number": "01P28882",
    "number": "V*031507E94441192588",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-yj36~ce93.tyth",
    ":version": "rv-x67d-qnvj~rstc",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1264214",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20080125",
    "violation_type_code": "E",
    "violation_number": "9444/234924",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20130731",
    "disposition_comments": "PVT: RESOLVED BY SATISFACTORY CAT 1 INSPECTION",
    "device_number": "01P28882",
    "number": "V*012508E9444/234924",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-z5u9-vbaf.nawy",
    ":version": "rv-fw73~z8nn.q3ua",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1359946",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20081113",
    "violation_type_code": "E",
    "violation_number": "9444/286139",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20150406",
    "disposition_comments": "PVT: SATISFIED BY SUBMISSION OF AOC FOR CAT 1 INSP",
    "device_number": "01P28882",
    "number": "V*111308E9444/286139",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-gyjj.5evv~2afq",
    ":version": "rv-drvf.2f2n_pzmn",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1492657",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20100426",
    "violation_type_code": "E",
    "violation_number": "9028/329960",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20150406",
    "disposition_comments": "PVT: SATISFIED BY SUBMISSION OF AOC FOR CAT 1 INSP",
    "device_number": "01P28882",
    "number": "V*042610E9028/329960",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-hz3i.v5g7-ufjg",
    ":version": "rv-i3z8.gg82_pzzj",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1559004",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20110211",
    "violation_type_code": "E",
    "violation_number": "9028/370781",
    "house_number": "416",
    "street": "WEST   23 STREET",
    "disposition_date": "20150406",
    "disposition_comments": "PVT: SATISFIED BY SUBMISSION OF AOC FOR CAT 1 INSP",
    "device_number": "01P28882",
    "number": "V*021111E9028/370781",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-igng~wstv~q8mi",
    ":version": "rv-vsyd_25v2.z52a",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "1711315",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20121024",
    "violation_type_code": "E",
    "violation_number": "9028/449851",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "disposition_date": "20150406",
    "disposition_comments": "PVT: SATISFIED BY SUBMISSION OF AOC FOR CAT 1 INSP",
    "device_number": "01P28882",
    "number": "V*102412E9028/449851",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-tbuu_m4wf.9jdx",
    ":version": "rv-5gv5-kbh6-jbvu",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "2035586",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20160112",
    "violation_type_code": "E",
    "violation_number": "9027/560099",
    "house_number": "416",
    "street": "WEST 23 STREET",
    "disposition_date": "20170713",
    "disposition_comments": "PVT: SATISFIED BY SUBMISSION OF AOC FOR CAT 1 INSP",
    "device_number": "01P28882",
    "number": "V*011216E9027/560099",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-b2uc-pstm~hgct",
    ":version": "rv-hwuc~nddk~3hy4",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "2138928",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20170113",
    "violation_type_code": "E",
    "violation_number": "9028/594636",
    "house_number": "416",
    "street": "W 23 ST",
    "disposition_date": "20170424",
    "disposition_comments": "PPN203 AOC SUB ON 3-8-17 BY LCD ELEVATOR       INSP. R. LICHT, CERT# 523001",
    "device_number": "1P28882",
    "number": "V*011317E9028/594636",
    "violation_category": "V*-DOB VIOLATION - Resolved",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-kcpq_wcks.e5gq",
    ":version": "rv-db7s-334s_gs7k",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  },
  {
    "isn_dob_bis_viol": "2439404",
    "boro": "1",
    "bin": "1012699",
    "block": "00720",
    "lot": "00055",
    "issue_date": "20200122",
    "violation_type_code": "E",
    "violation_number": "9028/667574",
    "house_number": "416",
    "street": "W 23 ST",
    "device_number": "1P28882",
    "number": "V012220E9028/667574",
    "violation_category": "V-DOB VIOLATION - ACTIVE",
    "violation_type": "E-ELEVATOR                                                        ELEVATORREQUIRED",
    ":id": "row-tx5v.uk3s.tykq",
    ":version": "rv-qq2r-8cbv-8mj6",
    ":created_at": "2025-03-03T14:15:14.576Z",
    ":updated_at": "2025-03-03T14:15:14.576Z"
  }
]
```

## API Documentation
- URL: `https://dev.socrata.com/foundry/data.cityofnewyork.us/3h2n-5cm9`

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
results = client.get("3h2n-5cm9", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
```