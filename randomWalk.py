import requests
import json
from random import randrange
from olivier import find_arrival
import datetime
from sys import stdout


def chooseDestination (depart , budget , date  , country = 'CH' , currency =  'CHF', locale = 'en-GB' , destination = 'anywhere' ) :
    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/'+str(destination)+'/'+str(date)+'/?apiKey=ha712564909427747796218296388326'


    r = requests.get(url)
    rjson = r.json()

    trips = rjson['Quotes']
    #print(trips)
    if(trips == []) :
        return False , []
    price = budget + 1
    count = 0
    maxIter = len(trips)*5


    while (price > budget ) :
        goodTrip = (trips[randrange(len(trips))])
        price = goodTrip['MinPrice']
        count += 1
        if ( count > maxIter ) :
            #print('error')
            return False ,[]

    arrived = goodTrip['OutboundLeg']['DestinationId']

    for place in rjson["Places"] :
        if (place['PlaceId'] == arrived) :
            goodTrip['arrived'] = place
            break

    goodTrip['arrivalTime'] = str(goodTrip['OutboundLeg']['DepartureDate'])
    return True ,goodTrip

def dateIncrease(date, increase):
    date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:]))
    date += datetime.timedelta(increase)
    return date.strftime("%Y-%m-%d")

def randomStep (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :

    (keepGoing , goodTrip) = chooseDestination(depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' )

    if (keepGoing) :

        return True , find_arrival(depart , goodTrip['arrived']['IataCode'], date)
    else :
        return False , []

#[{'name' : goodTrip['arrived']['Name'] ,
 #   'code' :  goodTrip['arrived']['SkyscannerCode'],
  #  'price' : goodTrip['MinPrice'],
   # 'arrivalDate' : goodTrip['arrivalTime'],
    #'departDate' : date,
    #'url' : ''
    #}]

def requestOneFinal (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    (finished , json) = randomStep(depart , budget , date)

def randomWalk (depart , budget , date , country = 'CH' , currency =  'CHF', locale = 'en-GB' , dayspercity=2) :
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

        while (not keepGoing) :
            count += 1


            #print(count , "count" , len(res))
            (keepGoing , tryStepList) =  randomStep (position , currentBudget , currentDate , country  , currency , locale  )


            if (keepGoing) :
                tryStep = tryStepList[0]

                position = tryStep['CodeEnding']
                currentBudget -= tryStep['Price']
                currentDate = dateIncrease(tryStep['ArrivalTime'][:10], dayspercity)

                res += [tryStep]

    canGoHome  = False

    print("Trying to go home.....\n")

    while (not canGoHome) :
        (canGoHome , goHome)  = chooseDestination (position , currentBudget , currentDate , country  , currency , locale , depart )
        if ( canGoHome) :
            goHome = find_arrival(position , depart , currentDate)[0]
            if ( currentBudget < goHome['Price'] ) :
                canGoHome = False
            else :
                res += [goHome]

        print(canGoHome , not canGoHome)

        if (not canGoHome) :
            print(res[-1])
            position = res[-1]['CodeBeginning']
            currentBudget += res[-1]['Price']
            res = res [ : -1]


    return res

truc = randomWalk('CDG', 2000, '2017-12-12', dayspercity=4)
print("\n\n")
for i in truc:
    print(i)
