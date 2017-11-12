def fast_getter(depart, budget, date, country = 'CH' , currency =  'CHF', locale = 'en-GB', dayspercity=2, marge=0):
    destlist=[]
    price=0
    fromcode=depart
    currdate=date
    enoughBudget = True
    current_budget = budget
    while (enoughBudget): #find route until no money
        dico={}
        (enoughBudget, destination) = chooseDestination(depart, current_budget, date)
        if(enoughBudget):
            dico['CodeBeginning'] = fromcode
            dico['DepartureDate']= currdate
            dico['Price']=destination['MinPrice']
            dico['CodeArrival'] = destination['arrived']['IataCode']
            dico['NameEnding'] = destination['arrived']['CityName']
            current_budget -= dico['Price']
            print(destination['MinPrice'], "to go to",dico['CodeArrival'], dico['NameEnding'])

            currdate=dateIncrease(currdate, 1)
            dico['ArrivalDate'] = currdate
            currdate=dateIncrease(currdate, dayspercity)
            destlist += [dico]


        canGoHome  = False

    print("Trying to go home.....\n")
    while (not canGoHome) : #come back until you can go home
        position = destlist[-1]['CodeArrival']
        print("Going from",position,"to",depart,"with budget",current_budget,"(adjusted to",current_budget+budget*marge,") at", currdate)
        (canGoHome , goHome)  = chooseDestination (position , current_budget+budget*marge , currdate , country=country  , currency=currency , locale=locale , destination=depart )
        if ( canGoHome) :
#             goHome = find_arrival(position , depart , currentDate)[0]
#             if ( currentBudget < goHomeCache['MinPrice'] ) :
#                 canGoHome = False
#             else :
            goHome ['NameEnding'] = goHome['arrived']['CityName']
            destlist += [goHome]

        else:

            position = destlist[-1]['CodeBeginning']
            current_budget += destlist[-1]['Price']
            destlist = destlist [ : -1]
            if (destlist == []) :
#                 print("RETURNING NONE")
                return []
    print("I am done")
    return destlist


def heavy_getter(depart, destination, budget, date, country = 'CH' , currency =  'CHF', locale = 'en-GB', dayspercity=2):
    travel=find_arrival(depart, destination, date)
    return travel
