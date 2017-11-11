import requests
import json
from random import randrange
def randomStep (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :

    r = requests.get('http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/anywhere/'+str(date)+'/?apiKey=ha712564909427747796218296388326')
    rjson = r.json()

    trips = rjson['Quotes']
    price = budget + 1 
    count = 0
    maxIter = len(trips)*5

    while (price > budget ) :
        goodTrip = (trips[randrange(len(trips))])
        price = goodTrip['MinPrice']
        count += 1 
        if ( count > maxIter) :
            print('error')
            return False ,[]

    if (goodTrip['Direct']  ) :
        arrived = goodTrip['OutboundLeg']['DestinationId']
    else :
        arrived = goodTrip['OutboundLeg'][-1]['DestinationId']

    for place in rjson["Places"] :
        if (place['PlaceId'] == arrived) :
            goodTrip['arrived'] = place
            break

    goodTrip['arrivalTime'] = str(goodTrip['OutboundLeg']['DepartureDate'])
    #print(goodTrip)
    return True , [{'name' : goodTrip['arrived']['Name'] ,
    'code' :  goodTrip['arrived']['IataCode'],
    'price' : goodTrip['MinPrice'],
    'url' : ''
    }]

def requestOneFinal (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    (finished , json) = randomStep(depart , budget , date)



