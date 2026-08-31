## Sample Get Users

## Purpose
To lookup one or more users in connecteam

## URI:
- Type: = `GET`
- Base URL = `https://api.connecteam.com/users/v1/users`


### Authorization
API Key In Header

### Headers
```json
{
    "accept": "application/json",
    "content-type": "application/json",
    "x-app-token": "{.env/CONNECTEAM_API_KEY}"
}
```

### Available Parameters
- `limit`: set to 500
- `offset`: set to 0 but increase as necessary for pagination
- `fullNames`
- `phoneNumbers`: formatted as '+1##########'
- `userStatus`: set to 'all'

## Sample cURL (Search by phoneNumbers)
```cURL
curl --request GET \
  --url 'https://api.connecteam.com/users/v1/users?limit=500&offset=0&phoneNumbers=%2015168041262&userStatus=all' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: ******'
```

## Sample cURL (Search by fullNames)
```cURL
curl --request GET \
  --url 'https://api.connecteam.com/users/v1/users?limit=500&offset=0&fullNames=paul%20licht&userStatus=all' \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'x-api-key: ******'
```

### Sample Response
```json
{
  "requestId": "e3b4988d-cf84-4d2f-a4aa-e816e2840917",
  "data": {
    "users": [
      {
        "firstName": "Paul",
        "lastName": "Licht",
        "phoneNumber": "+15168041262",
        "userType": "owner",
        "email": "paull@lcdelevator.com",
        "customFields": [
          {
            "customFieldId": 13475758,
            "value": [
              {
                "id": 1,
                "value": "Yes"
              }
            ],
            "type": "dropdown",
            "name": "OnboardingComplete"
          },
          {
            "customFieldId": 14375607,
            "value": "223",
            "type": "str",
            "name": "dbLink"
          },
          {
            "customFieldId": 15668170,
            "value": "R37465",
            "type": "str",
            "name": "PrestigeId"
          },
          {
            "customFieldId": 16491942,
            "value": [
              {
                "id": 1,
                "value": "10Yr"
              }
            ],
            "type": "dropdown",
            "name": "Honors Rec'd"
          },
          {
            "customFieldId": 30319328,
            "value": [
              {
                "id": 0,
                "value": "Employee"
              }
            ],
            "type": "dropdown",
            "name": "Worker Type"
          },
          {
            "customFieldId": 30319329,
            "value": [
              {
                "id": 1,
                "value": "Salaried"
              }
            ],
            "type": "dropdown",
            "name": "Pay Type"
          },
          {
            "customFieldId": 30319330,
            "value": [
              {
                "id": 1,
                "value": "Exempt"
              }
            ],
            "type": "dropdown",
            "name": "Overtime Eligibility"
          },
          {
            "customFieldId": 30319331,
            "value": [
              {
                "id": 0,
                "value": "Full Time"
              }
            ],
            "type": "dropdown",
            "name": "Employment Type"
          },
          {
            "customFieldId": 38531181,
            "value": "+15163158164",
            "type": "phone",
            "name": "Secondary Phone"
          },
          {
            "customFieldId": 38531182,
            "value": "paullicht89@gmail.com",
            "type": "email",
            "name": "Secondary Email"
          },
          {
            "customFieldId": 40522495,
            "value": [
              {
                "id": 5,
                "value": "Complete"
              }
            ],
            "type": "dropdown",
            "name": "HRIS Onboarding Classification"
          },
          {
            "customFieldId": 4688565,
            "value": "HR Director, Office Manager",
            "type": "str",
            "name": "Title"
          },
          {
            "customFieldId": 4688566,
            "value": "05/15/2011",
            "type": "date",
            "name": "Effective Hire Date"
          },
          {
            "customFieldId": 4688568,
            "value": [
              {
                "id": 7,
                "value": "HR"
              },
              {
                "id": 4,
                "value": "Office"
              }
            ],
            "type": "dropdown",
            "name": "Department"
          },
          {
            "customFieldId": 4688569,
            "value": [
              {
                "id": 4,
                "value": "Remote-FL"
              }
            ],
            "type": "dropdown",
            "name": "Location"
          },
          {
            "customFieldId": 4688571,
            "value": "04/12/1989",
            "type": "birthday",
            "name": "Birthday"
          },
          {
            "customFieldId": 9682336,
            "value": [
              {
                "id": 1,
                "value": "Default"
              }
            ],
            "type": "dropdown",
            "name": "PTO Accrual Type"
          },
          {
            "customFieldId": 9750541,
            "value": [
              {
                "id": 3,
                "value": "Mixed"
              }
            ],
            "type": "dropdown",
            "name": "Field/Office"
          },
          {
            "customFieldId": 9751443,
            "value": "74807f22-98a1-ec11-b400-0022480b8d8e",
            "type": "str",
            "name": "Fieldboss GUID"
          },
          {
            "customFieldId": 9751444,
            "value": "https://hris.lcd.nyc/employees",
            "type": "str",
            "name": "Coadvantage ID"
          },
          {
            "customFieldId": 9751445,
            "value": "063-76-3221",
            "type": "str",
            "name": "SSN"
          },
          {
            "customFieldId": 9752856,
            "value": "2010002",
            "type": "str",
            "name": "LCD ID"
          },
          {
            "customFieldId": 9791361,
            "value": "05/15/2011",
            "type": "date",
            "name": "OG Hire Date"
          },
          {
            "customFieldId": 9791394,
            "value": "1624 Wakefield Drive, Brandon, FL 33511",
            "type": "str",
            "name": "Address"
          },
          {
            "customFieldId": 9791398,
            "value": "recs69LvXdvXGIjG2",
            "type": "str",
            "name": "Airtable Record ID"
          },
          {
            "customFieldId": 9791563,
            "value": [
              {
                "id": 4,
                "value": "White"
              }
            ],
            "type": "dropdown",
            "name": "Race/Ethnicity"
          },
          {
            "customFieldId": 9791574,
            "value": [
              {
                "id": 3,
                "value": "Trade / Technical School Diploma / Certificate"
              }
            ],
            "type": "dropdown",
            "name": "Highest Level of Education Completed"
          },
          {
            "customFieldId": 9791665,
            "value": [
              {
                "id": 8,
                "value": "I am Not a Veteran or I do Not fall under any of the above"
              }
            ],
            "type": "dropdown",
            "name": "Veteran Status (VEVRAA - US Military Only)"
          },
          {
            "customFieldId": 9791696,
            "value": [
              {
                "id": 2,
                "value": "No"
              }
            ],
            "type": "dropdown",
            "name": "Vehicle Assigned"
          },
          {
            "customFieldId": 9791698,
            "value": [
              {
                "id": 1,
                "value": "Actively Working"
              }
            ],
            "type": "dropdown",
            "name": "Active Status"
          },
          {
            "customFieldId": 9791719,
            "value": [
              {
                "id": 4,
                "value": "Office"
              }
            ],
            "type": "dropdown",
            "name": "Trade Class"
          },
          {
            "customFieldId": 9791730,
            "value": [
              {
                "id": 6,
                "value": "N/A"
              }
            ],
            "type": "dropdown",
            "name": "License Class"
          },
          {
            "customFieldId": 9792561,
            "value": [
              {
                "id": 1,
                "value": "Employee"
              }
            ],
            "type": "dropdown",
            "name": "Employee Type"
          },
          {
            "customFieldId": 9793943,
            "value": [
              {
                "id": 1,
                "value": "N/A"
              }
            ],
            "type": "dropdown",
            "name": "PTO Custom Default"
          },
          {
            "customFieldId": 9794154,
            "value": 37.0,
            "type": "number",
            "name": "Age"
          },
          {
            "customFieldId": 9839591,
            "value": [
              {
                "id": 5,
                "value": "N/A"
              }
            ],
            "type": "dropdown",
            "name": "Clock Assignment"
          },
          {
            "customFieldId": 9888132,
            "value": [
              {
                "id": 0,
                "value": "Male"
              }
            ],
            "type": "dropdown",
            "name": "Gender"
          }
        ],
        "isArchived": false,
        "userId": 5676939,
        "kioskCode": "8846",
        "createdAt": 1692940679,
        "modifiedAt": 1785765515,
        "lastLogin": 1785499117,
        "smartGroupsIds": [
          1668483,
          1668484,
          1668496,
          7677911,
          7778004,
          7777806,
          7776748,
          7776746,
          7839573,
          7836200,
          7836244,
          7836344,
          7836370,
          7904934,
          7837730,
          7974235,
          7838271,
          7836537,
          13038232,
          13340957,
          7836571,
          7836593,
          7839510
        ],
        "invitedToBeManager": false,
        "mobileDevice": "samsung SM-S928U",
        "osVersion": "Other",
        "appVersion": "9.1.12.0",
        "mobileDeviceId": "6612310316076300"
      }
    ]
  },
  "paging": {
    "offset": 1,
    "total": 1
  }
}
```