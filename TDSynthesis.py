import requests
import time

###################

#print('Paste the address: ')
#address = input()

url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=10&occurred_after=2021-10-16T20%3A35%3A43.511Z"
headers = {"Accept": "application/json"}
seenTokens = []
while(1):
	response = requests.request("GET",url, headers=headers)


	data = response.json()
	for x in data['asset_events']:
		if (x['asset']['asset_contract']['symbol']!='OPENSTORE' and (x['asset']['token_id'] not in seenTokens)):
			print(x['asset']['asset_contract']['address']+" "+ x['asset']['token_id'] +" "+ x['asset']['asset_contract']['symbol'])
			seenTokens.append(x['asset']['token_id'])
	time.sleep(1)
