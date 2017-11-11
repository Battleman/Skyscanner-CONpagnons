import requests
import json
from random import randrange
def randomStep (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :

    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/anywhere/'+str(date)+'/?apiKey=ha712564909427747796218296388326'
    

    r = requests.get(url)
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
            #print('error')
            return False ,[]

    arrived = goodTrip['OutboundLeg']['DestinationId']

    for place in rjson["Places"] :
        if (place['PlaceId'] == arrived) :
            goodTrip['arrived'] = place
            break

    goodTrip['arrivalTime'] = str(goodTrip['OutboundLeg']['DepartureDate'])
    #print(goodTrip)
    return True , [{'name' : goodTrip['arrived']['Name'] ,
    'code' :  goodTrip['arrived']['SkyscannerCode'],
    'price' : goodTrip['MinPrice'],
    'date' : goodTrip['arrivalTime'],
    'url' : ''
    }]

def requestOneFinal (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    (finished , json) = randomStep(depart , budget , date)

def randomWalk (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    currentBudget = budget
    position = depart
    currentDate = date
    keepGoing = True
    res = []
    while (keepGoing) :
        
        keepGoing = False
        count = 0
        notSoGood = []

        while ((not keepGoing) and count < 15) :
            count += 1

            (keepGoing , tryStepList) =  randomStep (position , currentBudget , currentDate , country  , currency , locale  )
            
            

            if (keepGoing) :
                tryStep = tryStepList[0]
                position = tryStep['code']
                currentBudget -= tryStep['price']
                currentDate = tryStep['date'][:10]
            
                res += [tryStep]
                print(tryStep)

    print(res)
    return res
                
            
randomWalk ('EWR' , 500 , '2017-12-12'  )
