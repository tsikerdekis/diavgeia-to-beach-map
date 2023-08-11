import requests

BING_KEY = "AvU-kQHyioJBmXsT7T0H96XhSNPqxmmJhanur2HxxnF9cdKfHo_bT2RwtlsbWAAR"

def get_latlon(address):
    """
    Get the latitude and longitude of an address using the Bing Maps REST API
    DOES NOT WORK FOR Greece, GOOGLE MAPS API is pricey too, no other viable alternative
    """
    # url = 'https://dev.virtualearth.net/REST/v1/LocalSearch/?query=%s&userLocation=40.07094090125872,23.445713184826324&key=%s' % (address, BING_KEY)
    url = 'http://dev.virtualearth.net/REST/v1/Locations/?q=%s&maxResults=1&key=%s' % (address, BING_KEY)
    print(url)
    params = {'address': address}
    r = requests.get(url, params=params)
    print(r.json())
    results = r.json()['results']
    location = results[0]['geometry']['location']
    return location['lat'], location['lng']

print(get_latlon('Hotel Margarita, Kalithea, Greece'))