import requests
import time

###################

url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=1&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}
seenTokens = []

######
keyQueue = set()
minuteDict = {}
######

timer = 0
while(1):
	response = requests.request("GET",url, headers=headers)


	data = response.json()
	for x in data['asset_events']:
		if (x['asset']['asset_contract']['symbol']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens) and x['asset']['asset_contract']['schema_name']=='ERC721'):
			if (timer<60):
				pass
				#add to 1 minute column
			if (timer<240):
				pass
				#add to 5 minutes column
			if (timer<1200):
				pass
				#add to 20 minutes column
			if (timer<2400):
				pass
				#add to 40 minutes column
			if (timer<3600):
				pass
				#add to 1 hour column

			print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ x['asset']['asset_contract']['symbol'])
			seenTokens.append(x['asset']['token_id'])
			######
			keyQueue.add(timer)
			minuteDict[timer]={x['asset']['asset_contract']['symbol']}
			######
	timer+=1
	print(keyQueue)
	print(minuteDict)
	print(timer)
	time.sleep(1)

