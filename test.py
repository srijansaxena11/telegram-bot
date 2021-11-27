import requests

headers = {'content-type': 'text/plain', 'accept': 'application/json'}
requests.post('https://home.myopenhab.org/rest/items/Tubelight', 'ON', auth=requests.auth.HTTPBasicAuth('srijan.saxena0@gmail.com', 'srijan*1'), headers=headers)

r = requests.post(url, data=json.dumps(body), headers=headers)





requests.get('http://192.168.0.111:8080/rest/items/Tubelight/state')