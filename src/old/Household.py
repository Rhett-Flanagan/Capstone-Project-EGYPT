import random

class Household:
    __knowRad = 10 # knowledge radius used to determine how far a household can see
    __fieldLocs = []  # Contains tuples for the coordinates 
    __setNo = 0  # Designates which settlement a household belongs to
    __setLoc = (8, 6)  # Tuple giving coordinates of settlement
    __competency = 0.5 # Value denoting how able a household is to do tasks
    __ambition = 0.5  # Value denoting how likely a household is to take action
    __grain = 3000  # The amount of grain a household currently has
    __workers = 4  # The amount of workers available to harvest or farm
    __workerWorked = 0  # The amount of workers who have worked
    __genCountdown = 30  # The countdown until the next generation takes over and "changes" certain values
    __fieldsOwned = 0  # Number of fields owned by the household
    __fieldsHarvested = 0  # Number of fields harvested by the household
    __fissionChance = 0.3  # How likely a household is to split apart
    __genVariance = 0.9   #The change of variables between generations
    #__map  = Map()   # A map variable to connect the household to the greater simulation


    #def tick():


    def claimFields(self):
        claimChance = random.randon()
        if (((claimChance < Household.__ambition) and (Household.__workers > Household.__fieldsOwned)) or (Household.__fieldsOwned <=1)):
            currentGrain = Household.__grain
            #bestFertilityX =   unsure where "xcor" comes from
            #bestFertilityY =   unsure where "ycor" comes from
            bestFertility = 0

            # TODO calculate position to start in for household
            for i in range(Household.__knowRad):
                for j in range(Household.__knowRad):
                    # TODO Setup if to check if a settlement or river or owned land is hit  Unsure how it is represented in the map currently
                    #if (map.__grid[i][j] = settlement):
                        if (fertility > bestFertility):
                            bestFertilityX = i
                            bestFertilityY = j
                            bestFertility = fertility

            
            claimX = bestFertilityX
            claimY = bestFertilityY
            completeClaim(claimX, claimY)

    def completeClaim(claimX, claimY):
        #TODO Fill in 
        if (claimX <= map.__maxGrid) and (claimX > minMapX) and (claimY <=) and (claimX):
            claimed = False
            #TODO fill in how to identify what is on a patch
            if (map.__grid[claimX][claimY] != settlement) and ():
                #owned = True   Method should be in Patches
                #field = True   Method in patches
                #claimed = True  Method in patches
                #sproutFields = 1   Method in patches

                fieldsLoc.append((claimX, claimY))
                #setting up colours for linking  unsure of this till GUI implement
                #__harvested = false    patches variable
                #__yearsFallow = false   patches variable

                Household.__fieldsOwned += 1

    
    def farm(self):
        
        totalHarvest = 0
        maxPotentialYield = 2475
        #householdX = 
        #householdY = 
        househouldComp = Household.__competency
        Household.__workerWorked = 0
        Household.__fieldsHarvested = 0

        for i in range(Household.__workers/2):
            bestHarvest = 0
            
            for i in range(length(Household.__fieldLocs)):
                x, y = Household.__fieldLocs[i]

                #Requires field variables    Maybe we write a distance method to calculate distance from households to fields.   Unknown where distanceCost is stored
                thisHarvest = (__fertitlity*maxPotentialYield*househouldComp) - (distance(householdX, householdY, x, y)*distanceCost)
                if (__harvested = False) and (thisHarvest > bestHarvest):
                    bestField = (x, y)
                    bestHarvest = thisHarvest

            farmChance = random.random()

            if (Household.__grain < (Household.__workers*160)) or (farmChance < Household.__ambition*Household.__competency):
                bestX, bestY = bestField

                __harvested = True
                #set plant
                totalHarvest = totalHarvest + bestHarvest - 300

                Household.__workerWorked += 2
                Household.__fieldsHarvested += 1

        Household.__grain = Household.__grain + totalHarvest


    def rent(self):
        


    def consumeGrain(self):
        Household.__grain -= Household.__workers*160
        if (Household.__grain <= 0):
            Household.__grain = 0
            Household.__workers -= 1
            #Settlement.__pop -= 1
            #totalPop -= 1

            if Household.__workers <= 0:
                for i in range(length(Household.__fieldLocs)):
                   # __owned = False   unsure of iteraction between classes


    def storageLoss(self):
        Household.__grain = Household.__grain - (Household.__grain*0.1)
    

    def fieldChangeover(self):
        toDel = []
        for i in range(length(Household.__fieldLocs)):
            if (__harvested == True):
                __yearsFallow = 0
            else:
                __yearsFallow += 1
            
            if (__yearsFallow >= fallowLimit):   #unsure of where fallowLimit is
                __owned = False
                __field = False
                Household.__fieldsOwned -= 1
                toDel.append(i)

        for i in range(length(toDel):
            del Household.__fieldLocs[toDel[i]]

    
    def genChangeover(self):
        Household.__genCountdown -= 1

        if Household.__genCountdown <= 0:
            Household.__genCountdown = random.randint(5) + 10 

            ambitionChange = random.uniform(0, Household.__genVariance)
            decreaseChance = random.random()

            if (decreaseChance < 0.5):
                ambitionChange *= -1
            
            newAmbition = Household.__ambition + ambitionChange

            while(newAmbition > 1 or newAmbition < minAmbition):   ## not sure where minambition is being stored.
                 ambitionChange = random.uniform(0, Household.__genVariance)
                 decreaseChance = random.random()

                if (decreaseChance < 0.5):
                    ambitionChange *= -1
            
                 newAmbition = Household.__ambition + ambitionChange
            
            Household.__ambition = newAmbition



            competencyChange = random.uniform(0, Household.__genVariance)
            decreaseChance = random.random()

            if (decreaseChance < 0.5):
                competencyChange *= -1
            
            newComp = Household.__competency + competencyChange

            while(newComp > 1 or newComp < minComp):   ## not sure where minambition is being stored.
                competencyChange = random.uniform(0, Household.__genVariance)
                decreaseChance = random.random()

                if (decreaseChance < 0.5):
                    competencyChange *= -1
            
                newComp = Household.__competency + competencyChange
            
            Household.__competency = newComp

    #def fission(self):



            
            







