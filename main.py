import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
# import requests
import logging
# from uuid import uuid4
from telegram.utils.helpers import escape_markdown
import random
import time
from time import sleep
# from filters import CustomFilters
from commands import Commands
import sqlite3

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def setup(update, context):
    if(is_allowed(update)):
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Performing Setup. Please wait...')
        create_tables()
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Setup Done!')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def create_tables():
    conn = sqlite3.connect('telegram_bot.db')
    conn.execute("CREATE TABLE IF NOT EXISTS authorized_users (user_id bigint PRIMARY KEY NOT NULL, created_at datetime, updated_at datetime, lock_version int default 0)")
    conn.close()

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
            if user.id == int(authorized_user):
                allowed = True
                break  
        conn.close()
    return allowed

def authorize(update, context):
    allowed = False
    user = update.message.reply_to_message.from_user
    user_id = user.id
    conn = sqlite3.connect('telegram_bot.db')
    authorized_users = conn.execute("SELECT user_id FROM authorized_users WHERE lock_version<>-1")
    for authorized_user in authorized_users:
        if user.id == int(authorized_user):
            allowed = True
            break
    if allowed:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User already authorized.')
    else:
        conn.execute("INSERT INTO authorized_users(user_id,created_at,updated_at) VALUES(?,CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)")
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User authorized.')
    conn.close()

def unauthorize(update, context):
    allowed = False
    user = update.message.reply_to_message.from_user
    user_id = user.id
    conn = sqlite3.connect('telegram_bot.db')
    authorized_users = conn.execute("SELECT user_id FROM authorized_users WHERE lock_version<>-1")
    for authorized_user in authorized_users:
        if user.id == int(authorized_user):
            allowed = True
            break
    if allowed:
        conn.execute("UPDATE authorized_users set lock_version=-1, created_at= CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP where user_id=? and lock_version<>-1",user_id)
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User unauthorized.')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='User not authorized.')
    conn.close()

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
        current_temperature,feels_like_temperature = Commands.get_current_temperature()
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text=f'Current temperature in Lucknow is {current_temperature}°C. It feels like {feels_like_temperature}°C')
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
    user = update.message.from_user.id
    if(is_allowed(update)):
        context.bot.send_message(chat_id=update.message.chat_id, 
                        reply_to_message_id=None,
                        text="F**k you all!")
        chat_id=update.message.chat_id
        context.bot.leave_chat(chat_id)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')


def ip(update, context):
    if(is_allowed(update)):
        ip = Commands.get_ip()
        context.bot.send_message(chat_id=update.message.chat_id, 
                        reply_to_message_id=update.message.message_id,
                        text=f"Public IP address: {ip}")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def getfile(update, context):
    if(is_allowed(update)):
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
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')

def main():
    updater = Updater(os.environ["BOT_TOKEN"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('setup',setup))
    dp.add_handler(CommandHandler('authorize',authorize))
    dp.add_handler(CommandHandler('unauthorize',unauthorize))
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
#     dp.add_handler(MessageHandler(Filters.text, message_received)) #,CustomFilters.authorized_user))
#     dp.add_handler(MessageHandler(Filters.text, echo))
#     dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
