#!/usr/bin/env python

from client import ApiClient, ValidationError, AuthenticationError
import json
import config as keys
import geonamescache
import pytz
import datetime

# Function to call birth details
def run(path, isodatetime, coordinates):
    try:
        client = ApiClient(keys.CLIENT_ID, keys.CLIENT_SECRET)

        #  Detail Kundli endpoint :  /kundli/advanced
        url = f'v2/astrology/{path}'
        result = client.get(url, {
            'ayanamsa': 1,
            'coordinates': coordinates,        #'23.1765,75.7885' example of required format
            'datetime': isodatetime           #'2020-10-19T12:31:14+00:00', example of the required format
        })

# Extracting nakshatra name from the json api data
        # json_res = json.dumps(result)
        # res = json.loads(json_res)
        # data = res['data']
        # nak_details = data['nakshatra']




        # this code is used to save api response as data.json file you can find in this folder

        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)4''
        # print(nakshatra_details['nakshatra']['name'])

        # print(json.dumps(result))

    except ValidationError as e:
        for msg in e.getValidationMessages():
            print(msg['detail'])
    except AuthenticationError as e:
        print(e.message)
    return result

# Function to return detailed kundli
# def run2():
#     try:
#         client = ApiClient(keys.CLIENT_ID, keys.CLIENT_SECRET)

#         #  Detail Kundli endpoint :  /kundli/advanced

#         result = client.get('v2/astrology/kundli/advanced', {
#             'ayanamsa': 1,
#             'coordinates': '23.1765,75.7885',
#             'datetime': '2020-10-19T12:31:14+00:00',
#         })

#         # Printing the result of the response getting from the api
#         print(json.dumps(result, indent=4))

#         # this code is used to save api response as data.json file you can find in this folder

#         # with open('data.json', 'w', encoding='utf-8') as f:
#         #     json.dump(result, f, ensure_ascii=False, indent=4)4''

#         # print(json.dumps(result))

#     except ValidationError as e:
#         for msg in e.getValidationMessages():
#             print(msg['detail'])
#     except AuthenticationError as e:
#         print(e.message)
#     return result


# Coord function computes the coordinates of the bith place, converts the parameters into required format and passes them to the api function
def coord(city, date, time, path, ayanamsha):
    gc = geonamescache.GeonamesCache()
    city = gc.search_cities(city, case_sensitive=False)
    city1 = city[0]
# Computing latitude and longitude
    latitude = city1['latitude']
    longitude = city1['longitude']
    timezone = city1['timezone']
# Converting time into format required by prokerala params
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
    # print('hour-minute',hour,minute)
    coordinates = str(latitude) + ',' + str(longitude)
    # city_date = datetime.datetime(year, month, day).now(pytz.timezone(city_timezone)).isoformat()
    final_date_time = pytz.timezone(timezone).localize( datetime.datetime(year, month, day, hour, minute)).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
# Calling the run function and storing the data into a result variable
    result = run(path, final_date_time, coordinates)

    # json_res = json.dumps(result)
    # res = json.loads(json_res)
    # data = res['data']
    # nak_details = data['nakshatra']
    # nak_name = nak_details['name']

    return result















# if __name__ == '__main__':

    # run()