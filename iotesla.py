import json
from datetime import datetime, timedelta
from time import gmtime, strftime

global myemail

myemail = "my@email.com"


def tou_json(input_json):

    # Load input JSON data
    input_data = json.loads(input_json)

    # Extract start and end datetimes
    start_dt_str = input_data[0]["startDt"]
    end_dt_str = input_data[0]["endDt"]

    start_dt = datetime.fromisoformat(start_dt_str)
    end_dt = datetime.fromisoformat(end_dt_str)

    # Calculate the time difference
    time_difference = end_dt - start_dt

    date1 = start_dt.date()
    date2 = end_dt.date()

    if (date2 - date1).days == 1:
        print("Next Day")
        output_json = {
            "OFF_PEAK": [
                {
                    "toMinute": end_dt.minute,
                    "toDayOfWeek": 6,
                    "toHour": end_dt.hour,
                    "fromHour": 0,
                    "fromMinute": 0,
                    "fromDayOfWeek": 0
                },
                {
                    "toMinute": 0,
                    "toDayOfWeek": 6,
                    "toHour": 0,
                    "fromHour": start_dt.hour,
                    "fromMinute": start_dt.minute,
                    "fromDayOfWeek": 0
                }
            ],
            "ON_PEAK": [
                {
                    "fromDayOfWeek": 0,
                    "toDayOfWeek": 6,
                    "fromHour": end_dt.hour,
                    "fromMinute": end_dt.minute,
                    "toHour": start_dt.hour,
                    "toMinute": start_dt.minute
                }
            ]

        }
    else:
        print("Same Day")
        if (end_dt.minute == 30 and end_dt.hour == 23):
            print ("Ends at 23:30")        
            output_json = {
                "OFF_PEAK": [
                    {
                        "toMinute": 30,
                        "toDayOfWeek": 6,
                        "toHour": 5,
                        "fromHour": 0,
                        "fromMinute": 0,
                        "fromDayOfWeek": 0
                    },
                    {
                        "toMinute": end_dt.minute,
                        "toDayOfWeek": 6,
                        "toHour": end_dt.hour,
                        "fromHour": start_dt.hour,
                        "fromMinute": start_dt.minute,
                        "fromDayOfWeek": 0
                    },
                    {
                        "toMinute": 0,
                        "toDayOfWeek": 6,
                        "toHour": 0,
                        "fromHour": 23,
                        "fromMinute": 30,
                        "fromDayOfWeek": 0
                    }
                ],
                "ON_PEAK": [
                    {
                        "fromDayOfWeek": 0,
                        "toDayOfWeek": 6,
                        "fromHour": 5,
                        "fromMinute": 30,
                        "toHour": start_dt.hour,
                        "toMinute": start_dt.minute
                    }
                ]
            }
        else:
            output_json = {
                "OFF_PEAK": [
                    {
                        "toMinute": 30,
                        "toDayOfWeek": 6,
                        "toHour": 5,
                        "fromHour": 0,
                        "fromMinute": 0,
                        "fromDayOfWeek": 0
                    },
                    {
                        "toMinute": end_dt.minute,
                        "toDayOfWeek": 6,
                        "toHour": end_dt.hour,
                        "fromHour": start_dt.hour,
                        "fromMinute": start_dt.minute,
                        "fromDayOfWeek": 0
                    },
                    {
                        "toMinute": 0,
                        "toDayOfWeek": 6,
                        "toHour": 0,
                        "fromHour": 23,
                        "fromMinute": 30,
                        "fromDayOfWeek": 0
                    }
                ],
                "ON_PEAK": [
                    {
                        "fromDayOfWeek": 0,
                        "toDayOfWeek": 6,
                        "fromHour": 5,
                        "fromMinute": 30,
                        "toHour": start_dt.hour,
                        "toMinute": start_dt.minute
                    },
                    {
                        "fromDayOfWeek": 0,
                        "toDayOfWeek": 6,
                        "fromHour": end_dt.hour,
                        "fromMinute": end_dt.minute,
                        "toHour": 23,
                        "toMinute": 30
                    }
                ]
            }
    

    tarriffname = strftime("Go %Y%m%d %H%M%S", gmtime())

    sample_json = {
   "tou_settings":{
      "tariff_content":{
         "daily_charges":[
            {
               "name":"Charge",
               "amount":0
            }
         ],
         "demand_charges":{
            "ALL":{
               "ALL":0
            },
            "Summer":{

            },
            "Winter":{

            }
         },
         "utility":"Octopus",
         "energy_charges":{
            "ALL":{
               "ALL":0
            },
            "Summer":{
                "OFF_PEAK": 0.08,
                "ON_PEAK": 0.3
            },
            "Winter":{

            }
         },
         "name":tarriffname,
         "seasons":{
            "Summer":{
               "fromMonth":1,
               "fromDay":1,
               "toDay":31,
               "toMonth":12,
                "tou_periods": {}
            },
            "Winter":{
               "tou_periods":{

               }
            }
         },
         "sell_tariff":{
            "daily_charges":[
               {
                  "name":"Charge",
                  "amount":0
               }
            ],
            "demand_charges":{
               "ALL":{
                  "ALL":0
               },
               "Summer":{

               },
               "Winter":{

               }
            },
            "utility":"Octopus",
            "energy_charges":{
               "ALL":{
                  "ALL":0
               },
               "Summer":{
                    "OFF_PEAK": 0,
                    "ON_PEAK": 0
               },
               "Winter":{

               }
            },
            "name":tarriffname,
            "seasons":{
               "Summer":{
                  "fromMonth":1,
                  "fromDay":1,
                  "toDay":31,
                  "toMonth":12,
                  "tou_periods": {}
               },
               "Winter":{
                  "tou_periods":{

                  }
               }
            }
         }
      }
   }
}

    sample_json["tou_settings"]["tariff_content"]["seasons"]["Summer"]["tou_periods"].update(output_json)
    sample_json["tou_settings"]["tariff_content"]["sell_tariff"]["seasons"]["Summer"]["tou_periods"].update(output_json)

    # Display the converted JSON

    return sample_json


def send_tou_settings(json_data):

    import requests

    # Read the content from the original file
    with open('sites.json', 'r') as file:
        data = file.read()

    removedproduct = data.split(':',1)

    # Load the modified JSON data
    sitesjson = json.loads(removedproduct[1])

    mysite = sitesjson["energy_site_id"]
    print (mysite)

    "first string is: %s, second one is: %s"
    # API endpoint and JSON data
    api_url = "https://owner-api.teslamotors.com/api/1/energy_sites/%s/time_of_use_settings"  % (mysite)

    with open('cache.json') as f:
        cachejson = json.load(f)

    access_token = cachejson[myemail]["sso"]["access_token"]

    #print (access_token)

    # Step 2: Make a POST request to the API with the Bearer token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "User-Agent": "TeslaApp/4.8.0-1025/3e45238df4/android/11",
        "X-Tesla-User-Agent": "TeslaApp/4.8.0-1025/3e45238df4/android/11"
    }
    print(headers)
    print(json_data)
    api_response = requests.post(api_url, json=json_data, headers=headers)

    # Check the API response
    if api_response.status_code == 200:
        print("API request successful!")
        print(api_response.json())
    else:
        print(f"API request failed with status code {api_response.status_code}: {api_response.text}")



def loadjsonfiles():
    import os

    os.system("python cli.py -e %s -l > sites.json" % (myemail)) 
    os.system("python io.py > latest.json") 


if __name__ == '__main__':

    loadjsonfiles()

    with open('latest.json') as f:
        iojson = json.load(f)


    timesObj_val = iojson["timesObj"]
    timesObj = json.dumps(timesObj_val, indent=4)

    input_data = json.loads(timesObj)
    outputjson = tou_json(timesObj)

    print(json.dumps(outputjson, indent=4))

    send_tou_settings(outputjson)







