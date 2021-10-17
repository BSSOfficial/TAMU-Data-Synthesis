import requests
import time
import pandas as pd

###################
#url and headers for opensea api
url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}


seenTokens = [] #keep track of tokens that have already been seen so that we do not have duplicate rows


gatheringData = True

#export file for csv
file_name = "TAMUDataSynthesis.csv"
######

#this function utilizes pandas from the workshop in order to write the real time data to a file to be analyzed
def updateTable():
    global worksheet
    #create columns for dataframe
    df = pd.DataFrame(columns = ['Name', '1 Minute', '5 Minute', '15 Minute', '30 Minute', '1 Hour', '4 Hour','Session Total'])
    
    #creates rows and appends to dataframe
    for x in nameCounterDict:
        df = df.append({'Name' : x, '1 Minute' : nameCounterDict[x][0], '5 Minute' : nameCounterDict[x][1], '15 Minute' : nameCounterDict[x][2], '30 Minute' : nameCounterDict[x][3], '1 Hour' : nameCounterDict[x][4],'4 Hour' : nameCounterDict[x][5],'Session Total' : nameCounterDict[x][6]}, 
                ignore_index = True)

    #print df to terminal for current state and copy each time to csv to save in case of crash
    print(df.to_string(index=False))
    df.to_csv(file_name,index=False)

######
#key queues store the list of times necessary for checking against time intervals
keyQueue1 = []
keyQueue2 = []
keyQueue3 = []
keyQueue4 = []
keyQueue5 = []
keyQueue6 = []
#target Times are the times that the targets are found, then checked agains intervals and keyQueues to ensure data is real time
targetTimes = [0]*6

#dictionary time name relates the time found with the collections title
timeNameDict = {}
#dictionary name counter relates the name with the number of instances at specific intervals
nameCounterDict = {}
######


def beginGathering():
    global gatheringData
    #the purpose of this timer is to keep the event level to one, while our code can handle multiple, it was found to be more beneficial to just use one.
    timer = 0 

    #The contents of the while loop hold the functionality for gathering the data from the http GET request
    while(gatheringData):

    	#http GET request to opensea api
        response = requests.request("GET",url, headers=headers)
        
        #convert response to json for parsing
        data = response.json()

        #loop through each event to exclude certain types (i.e OPENSTORE, already seenTokens, anything but ERC721 transactions)
        for x in data['asset_events']:
            if (x['asset']['asset_contract']['name']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens) and x['asset']['asset_contract']['schema_name']=='ERC721'):
                #gather specific data such as name, address, and token id
                name = x['asset']['asset_contract']['name']
                print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ name)
                seenTokens.append(x['asset']['token_id'])
                ######
                #this is the functionality of keeping the limit of 1 transaction per cycle 
                if timer not in keyQueue1 and timer not in keyQueue2 and timer not in keyQueue3 and timer not in keyQueue4 and timer not in keyQueue5 and timer not in keyQueue6:
                    curTime=time.time()
                    keyQueue1.append(curTime)
                    timeNameDict[curTime]=name
                
                #initialize nameCounter dictionary
                if name in nameCounterDict:
                    nameCounterDict[name] = [x+1 for x in nameCounterDict[name]]
                else:
                    nameCounterDict[name] = [1,1,1,1,1,1,1]
                ######
            #this series of if's check the current time with the time found to ensure the data presented is real time
            #	this also allows us to see the minutes/hours that we found these transactions
            currentTime = time.time()
            if len(keyQueue1)>0:
                targetTimes[0] = keyQueue1[0]
                if targetTimes[0]+60<currentTime and targetTimes[0] in timeNameDict: #check time against 1 minute later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[0]]][0]-=1; #decrementer
                    keyQueue2.append(keyQueue1.pop(0)) #pass the reference of time to the next interval level
            if len(keyQueue2)>0:    
                targetTimes[1] = keyQueue2[0]
                if targetTimes[1]+300<currentTime and targetTimes[1] in timeNameDict:#check time against 5 minutes later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[1]]][1]-=1; #decrementer
                    keyQueue3.append(keyQueue2.pop(0)) #pass the reference of time to the next interval level
            if len(keyQueue3)>0:    
                targetTimes[2] = keyQueue3[0]
                if targetTimes[2]+900<currentTime and targetTimes[2] in timeNameDict:#check time against 15 minutes later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[2]]][2]-=1; #decrementer
                    keyQueue4.append(keyQueue3.pop(0)) #pass the reference of time to the next interval level
            if len(keyQueue4)>0:    
                targetTimes[3] = keyQueue4[0]
                if targetTimes[3]+1800<currentTime and targetTimes[3] in timeNameDict:#check time against 30 minutes later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[3]]][3]-=1; #decrementer
                    keyQueue5.append(keyQueue4.pop(0)) #pass the reference of time to the next interval level
            if len(keyQueue5)>0:
                targetTimes[4] = keyQueue5[0]
                if targetTimes[4]+3600<currentTime and targetTimes[4] in timeNameDict:#check time against 1 hour later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[4]]][4]-=1; #decrementer
                    keyQueue6.append(keyQueue5.pop(0)) #pass the reference of time to the next interval level
            if len(keyQueue6)>0:
                targetTimes[5] = keyQueue6[0]
                if targetTimes[5]+14400<currentTime and targetTimes[5] in timeNameDict:#check time against 4 hour later, decrement 1minute col counter
                    nameCounterDict[timeNameDict[targetTimes[5]]][5]-=1; #decrementer
                    keyQueue6.pop(0) #process final increment
                    timeNameDict.pop(targetTimes[5]) # remove the series from the list of future comparisons
        updateTable() #function call to update the table after each query
        timer+=1 #increment timer to ensure data consistency

        #print statements to ensure the internals are working properly as it writes
        print("Target Times for each minute comparison: "+str([targetTimes[0],targetTimes[1],targetTimes[2],targetTimes[3],targetTimes[4]]))
        print("Comparison Times: "+str([keyQueue1,keyQueue2,keyQueue3,keyQueue4,keyQueue5]))
        print(timeNameDict)
        print(nameCounterDict)

        time.sleep(1) #added to prevent api call overload and to ensure the data recieved is comprehendable

#function call to kickstart the data gathering process
beginGathering()