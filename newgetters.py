import requests
from random import randrange
from randomWalk import dateIncrease
from olivier import find_arrival
def chooseDestination_new (depart , budget , date , dayspercity=2 , country = 'CH' , currency =  'CHF', locale = 'en-GB' , destination = 'anywhere' ) :
    url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/'+str(country)+'/'+str(currency)+'/'+str(locale)+'/'+str(depart)+'/'+str(destination)+'/'+str(date)+'/?apiKey=ha712564909427747796218296388326'


    r = requests.get(url)
    rjson = r.json()

    trips = rjson['Quotes']

    if(trips == []) :
        return False , []

    price = budget + 1
    count = 0
    maxIter = len(trips)*5

    while (price > budget) :
        goodTrip = (trips[randrange(len(trips))])
        price = goodTrip['MinPrice']
        count += 1
        if ( count > maxIter ) :
            return False ,[]


    arrived = goodTrip['OutboundLeg']['DestinationId']

    for place in rjson["Places"] :
        if (place['PlaceId'] == arrived) :
            goodTrip['arrived'] = place
            break

    goodTrip['arrivalTime'] = str(goodTrip['OutboundLeg']['DepartureDate'])
    return True ,goodTrip


def fast_getter(depart, budget, date, country = 'CH' , currency =  'CHF', locale = 'en-GB', dayspercity=2, marge=0):
    destlist=[]
    price=0
    fromcode=depart
    currdate=date
    enoughBudget = True
    current_budget = budget
    while (enoughBudget): #find route until no money
        dico={}
        (enoughBudget, destination) = chooseDestination_new(fromcode, current_budget, currdate, )
        if(enoughBudget):
            dico['CodeBeginning'] = fromcode
            dico['DepartureDate']= currdate
            dico['Price']=destination['MinPrice']
            dico['CodeArrival'] = destination['arrived']['IataCode']
            dico['NameEnding'] = destination['arrived']['CityName']
            current_budget -= dico['Price']
            print(destination['MinPrice'], "to go to",dico['CodeArrival'], dico['NameEnding'])
            fromcode=dico['CodeArrival']
            currdate=dateIncrease(currdate, 1)
            dico['ArrivalDate'] = currdate
            currdate=dateIncrease(currdate, dayspercity)
            destlist += [dico]


        canGoHome  = False

    print("Trying to go home.....\n")
    while (not canGoHome) : #come back until you can go home
        position = destlist[-1]['CodeBeginning']
        print("Going from",position,"to",depart,"with budget",current_budget,"(adjusted to",current_budget+budget*marge,") at", currdate)
        (canGoHome , goHome)  = chooseDestination_new (position , current_budget+budget*marge , currdate , country=country  , currency=currency , locale=locale , destination=depart )
        if ( canGoHome) :
            # print(goHome)
            dico={}
            dico['CodeBeginning'] = fromcode
            dico['DepartureDate']= currdate
            dico['Price']=goHome['MinPrice']
            dico['CodeArrival'] = goHome['arrived']['IataCode']
            dico['NameEnding'] = goHome['arrived']['CityName']
            # current_budget -= dico['Price']
            # print(destination['MinPrice'], "to go to",dico['CodeArrival'], dico['NameEnding'])
            # currdate=dateIncrease(currdate, 1)
            dico['ArrivalDate'] = goHome['arrivalTime'][:10]
            # goHome ['NameEnding'] = goHome['arrived']['CityName']
            destlist += [dico]

        else:

            position = destlist[-1]['CodeBeginning']
            current_budget += destlist[-1]['Price']
            destlist = destlist [ : -1]
            if (destlist == []) :
#                 print("RETURNING NONE")
                return []
    print("I am done")
    return destlist


def heavy_getter(vols, country = 'CH' , currency =  'CHF', locale = 'en-GB', dayspercity=2):
    longlist = []
    for v in vols:
        print("\n\n",v)
        travel=find_arrival(v['CodeBeginning'], v['CodeArrival'], v['DepartureDate'])
        travel['NameEnding'] = v['NameEnding']
        longlist += [travel]
    return longlist

if __name__ == '__main__':
    dest = []
    while(True):
        dest = fast_getter("GVA", 400, "2017-12-20",marge=0.1)
        if(dest == []):
            print("I FAILED !! I AM NOT ROOT !! i will come back...")
        else:
            print(dest)
            break
    print("Now confirming, with heavy...")
    print("\n".join(heavy_getter(dest)))
