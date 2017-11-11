import requests
import json
from random import randrange
from olivier import find_arrival


def chooseDestination (depart , budget , date  , country = 'CH' , currency =  'CHF', locale = 'en-GB' , destination = 'anywhere' ) :
    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/'+str(destination)+'/'+str(date)+'/?apiKey=ha712564909427747796218296388326'

    print(url)

    r = requests.get(url)
    rjson = r.json()

    trips = rjson['Quotes']
    if(trips == []) :
        return False , []
    price = budget + 1
    count = 0
    maxIter = len(trips)*5
    
    print(trips)

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
    return True ,goodTrip

def randomStep (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :

    (keepGoing , goodTrip) = chooseDestination(depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' )
    print(goodTrip)
    print(chooseDestination(depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' , destination = goodTrip['arrived']['IataCode']))

    return True , find_arrival(depart , goodTrip['arrived']['IataCode'], date)

#[{'name' : goodTrip['arrived']['Name'] ,
 #   'code' :  goodTrip['arrived']['SkyscannerCode'],
  #  'price' : goodTrip['MinPrice'],
   # 'arrivalDate' : goodTrip['arrivalTime'],
    #'departDate' : date,
    #'url' : ''
    #}]

def requestOneFinal (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    (finished , json) = randomStep(depart , budget , date)

def randomWalk (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    currentBudget = budget
    position = depart
    currentDate = date
    keepGoing = True
    previousHome = None
    res = []
    while (keepGoing) :

        keepGoing = False
        count = 0
        notSoGood = []

        while ((not keepGoing) and count < 15) :
            count += 1

            print(position , currentBudget , currentDate , country  , currency , locale  )


            (keepGoing , tryStepList) =  randomStep (position , currentBudget , currentDate , country  , currency , locale  )


            #print(keepGoing , tryStepList)
            if (keepGoing) :
                count = 0
                # print(tryStepList)
                tryStep = tryStepList[0]
                #print('oulaoulala lal oulala    ',position , currentBudget , currentDate , country  , currency , locale , depart )
                #(canGoBack , toHome) =  chooseDestination (tryStep['CodeEnding'] , currentBudget , currentDate , country  , currency , locale , depart )

                if (True) :
                    #previousHome = toHome 
                    position = tryStep['CodeEnding']
                    currentBudget -= tryStep['Price']
                    currentDate = tryStep['ArrivalTime'][:10]

                    res += [tryStep]
                #else :
                 #   res += [previousHome]

    return res


print(randomWalk('GVA', 500, '2017-12-12'))
