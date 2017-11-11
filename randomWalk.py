import requests
import json
from random import randrange
from olivier import find_arrival
import datetime

def randomStep (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB') :

    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/anywhere/'+str(date)+'/?apiKey=ha712564909427747796218296388326'

    r = requests.get(url)
    rjson = r.json()
    # print("Having a step ",depart , budget , date," With rjson", rjson)
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

def dateIncrease(date, increase):
#     print(date[0:4], date[5:7], date[8:])
    # print(date)
    date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:]))
    date += datetime.timedelta(increase)
    return date.strftime("%Y-%m-%d")


def randomWalk (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB', dayspercity=2):
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

            (keepGoing , tryStepList) =  randomStep (position , currentBudget , currentDate , country  , currency , locale)


            if (keepGoing) :
                print("I found a trip : départure from {} at {}, arrival to {} at {}".format(position, currentDate, tryStepList[0]['CodeEnding'], tryStepList[0]['ArrivalTime'][:10]))
                tryStep = tryStepList[0]
                position = tryStep['CodeEnding']
                currentBudget -= tryStep['Price']
                currentDate = dateIncrease(tryStep['ArrivalTime'][:10], dayspercity)
                # print(currentDate)
                # print("new date ", currentDate)
                res += [tryStep]

    return res


for i in randomWalk('TIA', 2000, '2017-12-12', dayspercity=4):
    print(i)
