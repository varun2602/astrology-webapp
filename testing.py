from client import ApiClient, ValidationError, AuthenticationError
import json
import config as keys
import geonamescache

# Function to call birth details
def run(path, coordinates, date_time):
    try:
        client = ApiClient(keys.CLIENT_ID, keys.CLIENT_SECRET)

        #  Detail Kundli endpoint :  /kundli/advanced
        url = f'v2/astrology/{path}'
        result = client.get(url, {
            'ayanamsa': 1,
            'coordinates': coordinates,
            'datetime': date_time,
        })

        # Printing the result of the response getting from the api
        print(json.dumps(result, indent=4))

        # this code is used to save api response as data.json file you can find in this folder

        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(result, f, ensure_ascii=False, indent=4)4''

        # print(json.dumps(result))

    except ValidationError as e:
        for msg in e.getValidationMessages():
            print(msg['detail'])
    except AuthenticationError as e:
        print(e.message)
    return result



def coord():
    gc = geonamescache.GeonamesCache()
    city = gc.search_cities('wardha', case_sensitive=False)
    city1 = city[0]

    latitude = city1['latitude']
    longitude = city1['longitude']

    print(city)








