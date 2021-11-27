import os
import requests
import sqlite3
from requests import get
import pytz
from datetime import datetime
import json

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

  def get_ip():
    ip = get('https://api.ipify.org').content.decode('utf8')
    return ip

  def create_tables():
    conn = sqlite3.connect('telegram_bot.db')
    conn.execute("CREATE TABLE IF NOT EXISTS authorized_users (user_id bigint PRIMARY KEY NOT NULL, username varchar(100), created_at datetime, updated_at datetime, lock_version int default 0)")
    conn.close()

  def authorize_owner():
    conn = sqlite3.connect('telegram_bot.db')
    tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO authorized_users(user_id,username,created_at,updated_at) VALUES(?,?,?,?)",(int(os.environ["OWNER_ID"]),os.environ["OWNER_USERNAME"],current_time,current_time))
    conn.commit()
    conn.close()

  def switch_on(item):
    headers = {'content-type': 'text/plain', 'accept': 'application/json'}
    response = requests.post(f'https://home.myopenhab.org/rest/items/{item}', 'ON', auth=requests.auth.HTTPBasicAuth('srijan.saxena0@gmail.com', 'srijan*1'), headers=headers)
    return response.status_code

  def switch_off(item):
    headers = {'content-type': 'text/plain', 'accept': 'application/json'}
    response = requests.post(f'https://home.myopenhab.org/rest/items/{item}', 'OFF', auth=requests.auth.HTTPBasicAuth(os.environ["OPENHAB_USERNAME"], os.environ["OPENHAB_PASSWORD"]), headers=headers)
    return response.status_code

  def get_state(item):
    headers = {'content-type': 'text/plain', 'accept': 'application/json'}
    response = requests.get(f'https://home.myopenhab.org/rest/items/{item}', auth=requests.auth.HTTPBasicAuth(os.environ["OPENHAB_USERNAME"], os.environ["OPENHAB_PASSWORD"]), headers=headers)
    if response.status_code == 200:
      response_json = json.loads(response.text)
      state = response_json['state']
    else:
      state = ''
    return state
