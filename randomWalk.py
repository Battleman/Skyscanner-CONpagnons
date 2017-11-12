import requests
import json
from random import randrange
from olivier import find_arrival
import datetime
from sys import stdout


def toDate (date) :
    return datetime.datetime.strptime(date, "%Y-%m-%d")

def chooseDestination (depart , budget , dateBegin  , dateEnd , dayspercity , country = 'CH' , currency =  'CHF', locale = 'en-GB' , destination = 'anywhere' ) :
    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/'+str(destination)+'/'+str(dateBegin)+'/?apiKey=ha712564909427747796218296388326'


    r = requests.get(url)
    rjson = r.json()

    trips = rjson['Quotes']

    if(trips == []) :
        return False , []
    
    price = budget + 1
    count = 0
    maxIter = len(trips)*5

    d1 =toDate(dateBegin)
    end =toDate(dateEnd)

    coeffDivid = int( max (  ((end - d1).days) , 0 )  / dayspercity) + 1
    

       


    while (price > min(budget,budget / coeffDivid *1.25 )    ) :
        goodTrip = (trips[randrange(len(trips))])
        price = goodTrip['MinPrice']
        count += 1
        if ( count > maxIter ) :
            count = 0
            coeffDivid -= 1
            if (coeffDivid == 0):
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

def randomStep (depart , budget , dateBegin , dateEnd , dayspercity, country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :


    (keepGoing , goodTrip) = chooseDestination(depart , budget , dateBegin , dateEnd , dayspercity , country = 'CH' , currency =  'CHF', locale = 'en-GB' )


    if (keepGoing) :
        
        goodTrip['arrivalTime'] = str(goodTrip['OutboundLeg']['DepartureDate'])

        res = find_arrival(depart , goodTrip['arrived']['IataCode'], dateBegin)

        if ( toDate(dateEnd) < toDate(res[0]['ArrivalTime'][:10])) :
            return False , []
        else :
            for elem in res :

                elem['NameEnding'] = goodTrip['arrived']['CityName']

            return True , res
    else :
        return False , []

#[{'name' : goodTrip['arrived']['Name'] ,
 #   'code' :  goodTrip['arrived']['SkyscannerCode'],
  #  'price' : goodTrip['MinPrice'],
   # 'arrivalDate' : goodTrip['arrivalTime'],
    #'departDate' : date,
    #'url' : ''
    #}]

def requestOneFinal (depart , budget , dateBegin , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    (finished , json) = randomStep(depart , budget , dateBegin)

def randomWalk (depart , budget , dateBegin , dateEnd , dayspercity=2 , country = 'CH' , currency =  'CHF', locale = 'en-GB' ) :
    currentBudget = budget
    position = depart
    currentDate = dateBegin
    keepGoing = True
    previousHome = None
    res = []
    while (keepGoing) :

        keepGoing = False
        count = 0
        notSoGood = []
        


        (keepGoing , tryStepList) =  randomStep (position , currentBudget , currentDate , dateEnd , dayspercity, country  , currency , locale  )

        if (keepGoing) :
            tryStep = tryStepList[0]

            position = tryStep['CodeEnding']
            currentBudget -= tryStep['Price']
            currentDate = dateIncrease(tryStep['ArrivalTime'][:10], dayspercity)

            res += [tryStep]

    canGoHome  = False

    print("Trying to go home.....\n")
    

    while (not canGoHome) :
        currentDate = dateIncrease(res[-1]['ArrivalTime'][:10],dayspercity)
        (canGoHome , goHomeCache)  = chooseDestination (position , currentBudget , currentDate, dateEnd, dayspercity , country  , currency , locale , depart )
        if ( canGoHome) :
            goHome = find_arrival(position , depart , currentDate)[0]
            if ( currentBudget < goHome['Price'] or toDate(dateEnd) < toDate(goHome['ArrivalTime'][:10])) :
                canGoHome = False
            else :
                goHome ['NameEnding'] = goHomeCache['arrived']['CityName']
                res += [goHome]


        if (not canGoHome) :
            position = res[-1]['CodeBeginning']
            currentBudget += res[-1]['Price']
            res = res [ : -1]
            if (res == []) :
                return []


    return res


if __name__ == '__main__':
    truc = randomWalk('CDG', 1000, '2017-12-12', '2017-12-27' ,  dayspercity=4)
    print("\n\n")
    for i in truc:
        print(i)    


