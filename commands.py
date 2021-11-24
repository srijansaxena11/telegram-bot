import os
import requests

class Commands:
  def get_eth_rate_inr():
    print("Inside Commands.get_eth_rate_inr()")
    eth_api = requests.get(f'https://rest.coinapi.io/v1/exchangerate/ETH/INR?apikey={os.environ["COINAPI_KEY"]}').json()
    rate = eth_api['rate']
    return rate
  
  def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
  
  def get_current_temperature():
    temp_api = requests.get(f'https://api.openweathermap.org/data/2.5/weather?id=1264733&appid={os.environ["OPENWEATHERMAP_API_KEY"]}&units=metric').json()
    current_temperature = temp_api['main']['temp']
    feels_like_temperature = temp_api['main']['feels_like']
    return [current_temperature,feels_like_temperature]
