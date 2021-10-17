import requests
import time

###################

url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}
seenTokens = []

######
keyQueue1 = []
keyQueue2 = []
keyQueue3 = []
keyQueue4 = []
keyQueue5 = []
targetTimes = [0]*5
timeSymbolDict = {}
symbolCounterDict = {}
######

timer = 0
while(1):
	response = requests.request("GET",url, headers=headers)


	data = response.json()
	for x in data['asset_events']:
		if (x['asset']['asset_contract']['symbol']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens) and x['asset']['asset_contract']['schema_name']=='ERC721'):
			
			symbol = x['asset']['asset_contract']['symbol']
			print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ symbol)
			seenTokens.append(x['asset']['token_id'])
			######
			if timer not in keyQueue1 and timer not in keyQueue2 and timer not in keyQueue3 and timer not in keyQueue4 and timer not in keyQueue5:
				keyQueue1.append(timer)
				timeSymbolDict[timer]=symbol
			
			if symbol in symbolCounterDict:
				symbolCounterDict[symbol] = [x+1 for x in symbolCounterDict[symbol]]
			else:
				symbolCounterDict[symbol] = [1,1,1,1,1]
			######
		if len(keyQueue1)>0:
			targetTimes[0] = keyQueue1[0]
			if targetTimes[0]+2<timer and targetTimes[0] in timeSymbolDict:
				symbolCounterDict[timeSymbolDict[targetTimes[0]]][0]-=1;
				keyQueue2.append(keyQueue1.pop(0))
		if len(keyQueue2)>0:	
			targetTimes[1] = keyQueue2[0]
			if targetTimes[1]+6<timer and targetTimes[1] in timeSymbolDict:
				symbolCounterDict[timeSymbolDict[targetTimes[1]]][1]-=1;
				keyQueue3.append(keyQueue2.pop(0))
		if len(keyQueue3)>0:	
			targetTimes[2] = keyQueue3[0]
			if targetTimes[2]+12<timer and targetTimes[2] in timeSymbolDict:
				symbolCounterDict[timeSymbolDict[targetTimes[2]]][2]-=1;
				keyQueue4.append(keyQueue3.pop(0))
		if len(keyQueue4)>0:	
			targetTimes[3] = keyQueue4[0]
			if targetTimes[3]+18<timer and targetTimes[3] in timeSymbolDict:
				symbolCounterDict[timeSymbolDict[targetTimes[3]]][3]-=1;
				keyQueue5.append(keyQueue4.pop(0))
		if len(keyQueue5)>0:
			targetTimes[4] = keyQueue5[0]
			if targetTimes[4]+24<timer and targetTimes[4] in timeSymbolDict:
				symbolCounterDict[timeSymbolDict[targetTimes[4]]][4]-=1;
				keyQueue5.pop(0)
		
		
		
		
		
	timer+=1
	print([targetTimes[0],targetTimes[1],targetTimes[2],targetTimes[3],targetTimes[4]])
	print([keyQueue1,keyQueue2,keyQueue3,keyQueue4,keyQueue5])
	print(timeSymbolDict)
	print(symbolCounterDict)

	time.sleep(1)

