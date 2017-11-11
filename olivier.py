import requests
import time

def suggest_airport(airport, locale="en-GB", currency="chf", country="ch"):
    endpoint = 'http://partners.api.skyscanner.net/apiservices'
    token= 'ha712564909427747796218296388326'
    if type(airport) is not str:
        return []
    airports  = requests.get("{}/autosuggest/v1.0/{}/{}/{}?apikey={}&query={}".format(endpoint, country, currency, locale, token, airport))
    return airports.json()['Places']



def find_arrival(from_code, to_code, outboundDate, cabinclass="Economy", inboudDate="", adults=1, country="ch", locale="en-GB", currency="chf", children=0, infants=0):
    endpoint = 'http://partners.api.skyscanner.net/apiservices'
    token= 'ha712564909427747796218296388326'
    datadict={"cabinclass":cabinclass,"country":country,"currency":currency,"locale":locale,"originPlace":from_code,"locationSchema":"Iata",
          "destinationPlace":to_code,"outbounddate":outboundDate,"inbounddate":inboudDate,"adults":str(adults),"children":str(children),"infants":str(infants), "apikey":"ha712564909427747796218296388326"}
#     print(datadict)
    polling = requests.post("{}/pricing/v1.0".format(endpoint), data=datadict) #session creation
    if(polling.status_code != 201):
        return "ERROR POST: error " + str(polling.status_code)

    print('giuhjioji     ',polling.status_code)
    poll_address = polling.headers['Location']
    data = requests.get("{}?apikey={}&sortType=price&sortOrder=asc".format(poll_address,token))

    # print(data)
    while(data.status_code  !=  200  or data.json()['Status'] == "UpdatesPending"):
        print("Waiting...")
        time.sleep(1)
        data = requests.get("{}?apikey={}&sortType=price&sortOrder=asc".format(poll_address,token))


    results = []
    for itin in data.json()['Itineraries'][:4]:
        dico={}
        outboundLegId = itin['OutboundLegId']
        for leg in data.json()['Legs']:
            if(leg['Id'] == outboundLegId):
                dico['ArrivalTime']=leg['Arrival']
                dico['DepartureTime']=leg['Departure']
                break
        dico['DeepLink']=itin['PricingOptions'][0]['DeeplinkUrl']
        dico['Price'] = itin['PricingOptions'][0]['Price']
        dico['CodeBeginning'] = from_code
        dico['CodeEnding'] = to_code
        results += [dico]
    return results
