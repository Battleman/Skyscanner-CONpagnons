import requests
import time
from sys import stdout
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
    polling = requests.post("{}/pricing/v1.0".format(endpoint), data=datadict) #session creation
    if(polling.status_code != 201):
        return "ERROR"

    poll_address = polling.headers['Location']
    data = requests.get("{}?apikey={}&sortType=price&sortOrder=asc".format(poll_address,token))
    waitstring = "Waiting"
    i=0
    print("Doing a request, have code ", data.status_code)
    while(data.status_code  !=  200  or data.json()['Status'] == "UpdatesPending"):
        waitstring += "."
        i+=1
        print(waitstring, end='\r')
        stdout.flush()
        time.sleep(2)
        print("PASS {}, status is {}, headers are {}\n\n\n".format(i, data.status_code, "data.headers"))
        data = requests.get("{}?apikey={}&sortType=price&sortOrder=asc".format(poll_address,token))

    results = [] #list of dics
    for itin in data.json()['Itineraries'][:min(4, len(data.json()['Itineraries']))]:
        dico={}
        outboundLegId = itin['OutboundLegId']
        for leg in data.json()['Legs']:
            if(leg['Id'] == outboundLegId):
                dico['ArrivalTime']=leg['Arrival']
                dico['DepartureTime']=leg['Departure']
                break #no more match with be found in the Leg
        dico['DeepLink']=itin['PricingOptions'][0]['DeeplinkUrl']
        dico['Price'] = itin['PricingOptions'][0]['Price']
        dico['CodeBeginning'] = from_code
        dico['CodeEnding'] = to_code
        results += [dico]
    return results
