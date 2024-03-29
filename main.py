import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
import logging
# from uuid import uuid4
from telegram.utils.helpers import escape_markdown
import random
import time
from time import sleep
from commands import Commands
import sqlite3
import pytz
from datetime import datetime
import psutil
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def setup(update, context):
    if(is_owner(update)):
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Performing Setup. Please wait...')
        Commands.create_tables()
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Setup Done!')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def is_owner(update):
    allowed = False
    user = update.message.from_user
    if user.id == int(os.environ["OWNER_ID"]):
        allowed = True
    return allowed

def is_allowed(update):
    allowed = False
    if is_owner(update):
        allowed = True
    else:
        user = update.message.from_user
        conn = sqlite3.connect('telegram_bot.db')
        authorized_users = conn.execute("SELECT user_id FROM authorized_users WHERE lock_version<>-1")
        for authorized_user in authorized_users:
            if user.id == int(authorized_user[0]):
                allowed = True
                break  
        conn.close()
    return allowed

def authorize(update, context):
    if(is_owner(update)):
        allowed = False
        user = update.message.reply_to_message.from_user
        user_id = user.id
        username = user.username
        conn = sqlite3.connect('telegram_bot.db')
        authorized_users = conn.execute("SELECT user_id FROM authorized_users WHERE lock_version<>-1")
        for authorized_user in authorized_users:
            if int(user_id) == int(authorized_user[0]):
                allowed = True
                break
        if allowed:
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User already authorized.')
        else:  
            tz = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            conn.execute("INSERT INTO authorized_users(user_id,username,created_at,updated_at) VALUES(?,?,?,?)",(int(user_id),username,current_time,current_time))
            conn.commit()
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User authorized.')
        conn.close()
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def unauthorize(update, context):
    if(is_owner(update)):
        allowed = False
        user = update.message.reply_to_message.from_user
        user_id = user.id
        conn = sqlite3.connect('telegram_bot.db')
        authorized_users = conn.execute("SELECT user_id FROM authorized_users WHERE lock_version<>-1")
        for authorized_user in authorized_users:
            if int(user_id) == int(authorized_user[0]):
                allowed = True
                break
        if allowed:
            tz = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
            conn.execute("UPDATE authorized_users set lock_version=-1, created_at= ?, updated_at=? where user_id=? and lock_version<>-1",(int(user_id),current_time,current_time))
            conn.commit()
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User unauthorized.')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User not authorized.')
        conn.close()
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def listauthusers(update, context):
    # if(is_allowed(update)):
    authorized_usernames_array = []
    conn = sqlite3.connect('telegram_bot.db')
    authorized_users = conn.execute("SELECT user_id,username FROM authorized_users WHERE lock_version<>-1")
    for authorized_user in authorized_users:
        authorized_usernames_array.append(f'@{authorized_user[1]}')
    conn.close()
    authorized_usernames_string='\n'.join(authorized_usernames_array)
    context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'List of authorized users:\n{authorized_usernames_string}')
    # else:
    #     context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')


def stark(update, context):
    if(is_allowed(update)):
        f = open("tony_stark_quotes.txt","r")
        r = random.randint(0,49)
        lines = f.readlines()
        quote = lines[r]
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=quote)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def eth(update, context):
    if(is_allowed(update)):
        print("Inside eth()")
        rate = str(Commands.get_eth_rate_inr()).split('.')[0]
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Current price of Ethereum is Rs. {rate}')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def bop(update, context):
    if(is_allowed(update)):
        url = Commands.get_url()
        chat_id = update.message.chat_id
        context.bot.send_photo(chat_id=chat_id, photo=url)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def start(update, context):
    if(is_allowed(update)):
        Commands.is_chat_listed(update)
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="Hello. Good Morning/Noon/Evening, whatever it is. I am a bot if you didn't notice. I am developed to as a fun hobby and to test out a few things. Also I'm not a regular bot. I'm a part time bot. I may not even respond at certain times.")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def echo(update, context):
    if(is_allowed(update)):
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=update.message.text)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def message_received(update, context):
#     print("Inside message_received()")
#    if ((update.message.text.find("srijan") != -1) and ((update.message.text.find("sleep") != -1) or (update.message.text.find("wake") != -1) or (update.message.text.find("woke") != -1))):
#        f = open("/home/openhabian/isSleeping","r")
#        if (f.read()=="1\n"):
#            bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="Yes, Srijan sir is sleeping currently. Don't you dare to disturb him.")
#        else:
#            bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="No, Srijan sir is not sleeping currently. He may ignore you nonetheless.")
    if(is_allowed(update)):
        if ((update.message.text.find("hi") != -1) or (update.message.text.find("hello") != -1)):
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="You are trying to initiate a conversation with a bot? You seriously need to find a hobby.")
        elif (update.message.text.find("bye") != -1):
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="I don't even know you.")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="Either you are dumb or I am. I am bot in my initial phase and being worked upon. So fingers on you.\nP.S.: Command doesn't exist. Let @SrijanSaxena know to add the required command. ")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def inlinequery(bot, update):
    print("Inside inlinequery()")
    """Handle the inline query."""
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Query",
            input_message_content=InputTextMessageContent(
                query))]
    update.inline_query.answer(results)
    
def ping(update, context):
    if(is_allowed(update)):
        start_time = int(round(time.time() * 1000))
        reply = context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text="Starting Ping") #context.bot.send_message("Starting Ping", context.bot, update)
        end_time = int(round(time.time() * 1000))
        context.bot.edit_message_text(text=f'{end_time - start_time} ms', message_id=reply.message_id,
                                  chat_id=reply.chat.id,
                                  parse_mode='HTMl')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
        
def countdown(update, context):
    if(is_allowed(update)):
        message_args = update.message.text.split(' ')
        try:
            time = message_args[1]
        except IndexError:
            time = 0

        if (time.find('s') == -1):
            if (time.find('m') == -1):
                if (time.find('h') == -1):
                    time_in_seconds = 0
                else:
                    #code for time in hours
                    try:
                        time_in_hours = int(time.split('h')[0])
                    except IndexError:
                        time_in_hours = 0
                    time_in_seconds = time_in_hours*3600
            else:
                #code for time in minutes
                try:
                    time_in_minutes = int(time.split('m')[0])
                except IndexError:
                    time_in_minutes = 0
                time_in_seconds = time_in_minutes*60
        else:
            #code for time in seconds
            try:
                time_in_seconds = int(time.split('s')[0])
            except IndexError:
                time_in_seconds = 0
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Starting countdown for {time_in_seconds} seconds')
        reply = context.bot.send_message(chat_id=update.message.chat_id, text=time_in_seconds) 
        while(time_in_seconds>0):
            sleep(1)
            time_in_seconds-=1
            context.bot.edit_message_text(text=time_in_seconds, message_id=reply.message_id,
                                  chat_id=reply.chat.id)

        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Countdown finished')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def temperature(update, context):
    if(is_allowed(update)):
        message_args = update.message.text.split(' ')
        try:
            city = message_args[1]
        except IndexError:
            city = ''
        if city == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide a city name to get temperature details.')
        else:
            current_temperature,feels_like_temperature = Commands.get_current_temperature(city)
            if (current_temperature==False or feels_like_temperature==False):
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'There was an error in retrieving the details for {city}. Please check the city name again.')
            else:
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Current temperature in {city} is {current_temperature}°C. It feels like {feels_like_temperature}°C')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
        
def info(update, context):
    if(is_allowed(update)):
        try:
            user = update.message.reply_to_message.from_user
            user_id = user.id
            is_user_bot = user.is_bot
            user_first_name = user.first_name
            user_last_name = user.last_name if user.last_name is not None else ''
            user_username  = user.username if user.username is not None else ''
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, 
                                     text=f'<b>User ID</b>: {user_id}\n<b>Is User Bot</b>: {is_user_bot}\n<b>User First Name</b>: {user_first_name}\n<b>User Last Name</b>: {user_last_name}\n<b>User username</b>: @{user_username}', 
                                     parse_mode='HTML')
        except:
            chat_id = update.message.chat_id
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Current Chat ID: {chat_id}')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
        
def leave(update, context):
    if(is_owner(update)):
        context.bot.send_message(chat_id=update.message.chat_id, 
                        reply_to_message_id=None,
                        text="F**k you all!")
        chat_id=update.message.chat_id
        context.bot.leave_chat(chat_id)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def ip(update, context):
    if(is_allowed(update)):
        ip = Commands.get_ip()
        context.bot.send_message(chat_id=update.message.chat_id, 
                        reply_to_message_id=update.message.message_id,
                        text=f"Public IP address: `{ip}`",parse_mode='markdown')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def getfile(update, context):
    if(is_owner(update)):
        message_args = update.message.text.split(' ')
        try:
            file_name = message_args[1]
        except IndexError:
            file_name = ''
        if file_name == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide the file name to download.')
        else:
            file = open(file_name, 'rb')
            context.bot.sendDocument(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, document=file)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def on(update, context):
    if(is_owner(update)):
        message_args = update.message.text.split(' ')
        try:
            item = message_args[1]
        except IndexError:
            item = ''
        if item == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide the item name to switch on.')
        else:
            response_code = Commands.switch_on(item)
            if response_code == 200:
                message_to_be_sent = f'Successfully switched on {item}'
            else:
                message_to_be_sent = f'There was an error switching on {item}. Please check the item name again.'
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=message_to_be_sent)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def off(update, context):
    if(is_owner(update)):
        message_args = update.message.text.split(' ')
        try:
            item = message_args[1]
        except IndexError:
            item = ''
        if item == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide the item name to switch off.')
        else:
            response_code = Commands.switch_off(item)
            if response_code == 200:
                message_to_be_sent = f'Successfully switched off {item}'
            else:
                message_to_be_sent = f'There was an error switching off {item}. Please check the item name again.'
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=message_to_be_sent)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def state(update, context):
    if(is_owner(update)):
        message_args = update.message.text.split(' ')
        try:
            item = message_args[1]
        except IndexError:
            item = ''
        if item == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide the item name to check state.')
        else:
            state = Commands.get_state(item)
            if state == '':
                message_to_be_sent = f'There was an error in retrieving the state of {item}. Please check the item name again.'
            else:
                message_to_be_sent = f'{item} is currently {state}.'
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=message_to_be_sent)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def hwinfo(update, context):
    if(is_allowed(update)):
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def details(update, context):
    if(is_allowed(update)):
        message_args = update.message.text.split(' ')
        try:
            user_id = int(message_args[1])
        except IndexError:
            user_id = ''
        if user_id == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Provide the user id to get the details.')
        else:
            user_details = context.bot.get_chat(user_id)
            user_first_name = user_details.first_name
            user_last_name = user_details.last_name if user_details.last_name is not None else ''
            user_username  = user_details.username if user_details.username is not None else ''
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, 
                                     text=f'<b>User ID</b>: {user_id}\n<b>User First Name</b>: {user_first_name}\n<b>User Last Name</b>: {user_last_name}\n<b>User username</b>: @{user_username}', 
                                     parse_mode='HTML')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def send(update, context):
    if(is_owner(update)):
        message_args = update.message.text.replace('/send ', '').split('#')
        try:
            chat_id = int(message_args[0])
            message_to_be_sent = message_args[1]
        except IndexError:
            chat_id = 0
            message_to_be_sent = ''
        if chat_id == 0 or message_to_be_sent == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Wrong arguments passed. Command syntax:\n/send <Chat ID>#<Meesage to be sent>')
        else:
            context.bot.send_message(chat_id=chat_id, text=message_to_be_sent)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def listchats(update, context):
    if(is_owner(update)):
        chats_list = {}
        conn = sqlite3.connect('telegram_bot.db')
        chats = conn.execute("SELECT chat_id,chat_name FROM chat_lists WHERE lock_version<>-1")
        for chat in chats:
            chats_list[chat[0]]=chat[1]
        conn.close()
        chats_list_string = ''
        for i in chats_list:
            chats_list_string+=f'`{i}` : {chats_list[i]}\n'
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'List of chats:\n{chats_list_string}',parse_mode='markdown')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not the owner.')

def ethstats(update, context):
    if(is_allowed):
        message_args = update.message.text.split(' ')
        try:
            miner_id = message_args[1]
        except IndexError:
            miner_id = ''
        if miner_id == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Provide the ethereum wallet ID to get the details from ethermine.org')
        else:    
            eth_miner_stats, eth_worker_stats = Commands.get_eth_miner_stats(miner_id)
            if eth_miner_stats == '' or eth_worker_stats == '':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'There was an error in retrieving the details of miner with ethereum wallet ID: {miner_id}. Please check the ethereum wallet ID again.')
            else:
                # eth_miner_stats = eth_miner_stats.json()
                # eth_worker_stats = eth_worker_stats.json()
                current_hash_rate = float(eth_miner_stats['currentHashrate'])/1000000
                reported_hash_rate = float(eth_miner_stats['reportedHashrate'])/1000000
                active_workers = eth_miner_stats['activeWorkers']
                unpaid_balance = float(eth_miner_stats['unpaid'])/100000000000000000
                eth_miner_stats_msg = f'Current Hashrate: {current_hash_rate} MH/s\nReported Hashrate: {reported_hash_rate} MH/s\nActive Workers: {active_workers}\nUnpaid Balance: {unpaid_balance} ETH'
                eth_worker_stats_msg = ''
                for eth_worker_stat in eth_worker_stats:
                    worker_name = eth_worker_stat['worker']
                    current_hash_rate = float(eth_worker_stat['currentHashrate'])/1000000
                    reported_hash_rate = float(eth_worker_stat['reportedHashrate'])/1000000
                    eth_worker_stats_msg += f'Worker Name: {worker_name}\nCurrent Hashrate: {current_hash_rate} MH/s\nReported Hashrate: {reported_hash_rate} MH/s\n\n'
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Ethereum Miner stats from ethermine.org:\nEthereum wallet ID: `{miner_id}`\n\n{eth_miner_stats_msg}\n\n{eth_worker_stats_msg}',parse_mode='markdown')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def do(update, context):
    if(is_allowed(update)):
        message_args = update.message.text.split(' ')
        try:
            action = message_args[1]
        except IndexError:
            action = ''
        if action == '':
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Provide the action name.')
        else:
            if action == 'lenny':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='( ͡° ͜ʖ ͡°)')
            elif action == 'sad':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='⊙﹏⊙')
            elif action == 'annoyed':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='(¬_¬)')
            elif action == 'cry':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='(ಥ﹏ಥ)')
            elif action == 'shrug':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='¯\\_(ツ)_/¯') 
            # elif action == 'shoot':
            #     context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='̿ ̿ ̿'̿'\\̵͇̿̿\\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿')
            elif action == 'happy':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='(¬‿¬)')
            elif action == 'wink':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='◕‿↼')
            elif action == 'f':
                msg = "....................../´¯/) \n....................,/¯../ \n.................../..../ \n............./´¯/'...'/´¯¯`·¸ \n........../'/.../..../......./¨¯\\ \n........('(...´...´.... ¯~/'...') \n.........\\.................'...../ \n..........''...\\.......... _.·´ \n............\\..............( \n..............\\.............\\..."
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=msg)
            elif action == 'another action':
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='another action')
            else:
                context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Action not found')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
    

def main():
    updater = Updater(os.environ["BOT_TOKEN"])
    Commands.create_tables()
    Commands.authorize_owner(updater)
    Commands.authorize_users(updater)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('setup',setup))
    dp.add_handler(CommandHandler('auth',authorize))
    dp.add_handler(CommandHandler('unauth',unauthorize))
    dp.add_handler(CommandHandler('listauthusers',listauthusers))
    dp.add_handler(CommandHandler('start',start)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('eth',eth)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('bop',bop)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('ping',ping)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('countdown',countdown)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('stark',stark)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('temp',temperature)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('info',info))
    dp.add_handler(CommandHandler('leave',leave))
    dp.add_handler(CommandHandler('ip',ip))
    dp.add_handler(CommandHandler('getfile',getfile))
    dp.add_handler(CommandHandler('on',on))
    dp.add_handler(CommandHandler('off',off))
    dp.add_handler(CommandHandler('state',state))
    dp.add_handler(CommandHandler('hwinfo',hwinfo))
    dp.add_handler(CommandHandler('details',details))
    dp.add_handler(CommandHandler('send',send))
    dp.add_handler(CommandHandler('listchats',listchats))
    dp.add_handler(CommandHandler('ethstats',ethstats))
    dp.add_handler(CommandHandler('do',do))
#     dp.add_handler(MessageHandler(Filters.text, message_received)) #,CustomFilters.authorized_user))
#     dp.add_handler(MessageHandler(Filters.text, echo))
#     dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
