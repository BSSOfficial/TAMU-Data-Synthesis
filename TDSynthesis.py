import requests




###################

print('Paste the address: ')
address = input()


url = "https://api.opensea.io/api/v1/events?asset_contract_address="+address+"&only_opensea=false&offset=0&limit=20"
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers)
file = open("testData.txt", 'w')
file.write(response.text)