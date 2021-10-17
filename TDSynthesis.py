import requests
import time
import pandas as pd


###################

url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}
seenTokens = []


gatheringData = True

######

def updateTable():
    global worksheet
    df = pd.DataFrame(columns = ['Name', 'oneMinute', 'fiveMinute', 'twentyMinute', 'fortyMinute', 'sixtyMinute'])
    
    for x in nameCounterDict:
        df = df.append({'Name' : x, 'oneMinute' : nameCounterDict[x][0], 'fiveMinute' : nameCounterDict[x][1], 'twentyMinute' : nameCounterDict[x][2], 'fortyMinute' : nameCounterDict[x][3], 'sixtyMinute' : nameCounterDict[x][4]}, 
                ignore_index = True)
    print(df.to_string(index=False))

######
keyQueue1 = []
keyQueue2 = []
keyQueue3 = []
keyQueue4 = []
keyQueue5 = []
targetTimes = [0]*5
timeNameDict = {}
nameCounterDict = {}
######


def beginGathering():
	global gatheringData
	timer = 0
	while(gatheringData):
		response = requests.request("GET",url, headers=headers)
		

		data = response.json()
		for x in data['asset_events']:
			if (x['asset']['asset_contract']['name']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens) and x['asset']['asset_contract']['schema_name']=='ERC721'):
				
				name = x['asset']['asset_contract']['name']
				print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ name)
				seenTokens.append(x['asset']['token_id'])
				######
				if timer not in keyQueue1 and timer not in keyQueue2 and timer not in keyQueue3 and timer not in keyQueue4 and timer not in keyQueue5:
					keyQueue1.append(timer)
					timeNameDict[timer]=name
				
				if name in nameCounterDict:
					nameCounterDict[name] = [x+1 for x in nameCounterDict[name]]
				else:
					nameCounterDict[name] = [1,1,1,1,1]
				######
			if len(keyQueue1)>0:
				targetTimes[0] = keyQueue1[0]
				if targetTimes[0]+2<timer and targetTimes[0] in timeNameDict:
					nameCounterDict[timeNameDict[targetTimes[0]]][0]-=1;
					keyQueue2.append(keyQueue1.pop(0))
			if len(keyQueue2)>0:	
				targetTimes[1] = keyQueue2[0]
				if targetTimes[1]+6<timer and targetTimes[1] in timeNameDict:
					nameCounterDict[timeNameDict[targetTimes[1]]][1]-=1;
					keyQueue3.append(keyQueue2.pop(0))
			if len(keyQueue3)>0:	
				targetTimes[2] = keyQueue3[0]
				if targetTimes[2]+12<timer and targetTimes[2] in timeNameDict:
					nameCounterDict[timeNameDict[targetTimes[2]]][2]-=1;
					keyQueue4.append(keyQueue3.pop(0))
			if len(keyQueue4)>0:	
				targetTimes[3] = keyQueue4[0]
				if targetTimes[3]+18<timer and targetTimes[3] in timeNameDict:
					nameCounterDict[timeNameDict[targetTimes[3]]][3]-=1;
					keyQueue5.append(keyQueue4.pop(0))
			if len(keyQueue5)>0:
				targetTimes[4] = keyQueue5[0]
				if targetTimes[4]+24<timer and targetTimes[4] in timeNameDict:
					nameCounterDict[timeNameDict[targetTimes[4]]][4]-=1;
					keyQueue5.pop(0)
					if nameCounterDict[timeNameDict[targetTimes[4]]][4] == 0:
						nameCounterDict.pop(timeNameDict[targetTimes[4]])
					timeNameDict.pop(targetTimes[4])
		updateTable()
		timer+=1
		print("Target Times for each minute comparison: "+str([targetTimes[0],targetTimes[1],targetTimes[2],targetTimes[3],targetTimes[4]]))

		print([keyQueue1,keyQueue2,keyQueue3,keyQueue4,keyQueue5])
		print(timeNameDict)
		print(nameCounterDict)

		time.sleep(1)


beginGathering()






