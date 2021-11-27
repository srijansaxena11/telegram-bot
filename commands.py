import os
import requests
import sqlite3
from requests import get

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
