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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def is_allowed(update):
    allowed = False
    user = update.message.from_user
    if user.id in [int(os.environ["OWNER_ID"])]:
        allowed = True
    return allowed

# def get_eth_rate_inr():
#     print("Inside get_eth_rate_inr()")
#     eth_api = requests.get('https://rest.coinapi.io/v1/exchangerate/ETH/INR?apikey=95CBCBB3-72EB-48D3-B60D-9DDCB21F70AF').json()
#     rate = eth_api['rate']
#     return rate

# def get_url():
#     contents = requests.get('https://random.dog/woof.json').json()
#     url = contents['url']
#     return url

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

# def get_current_temperature():
#     temp_api = requests.get('https://api.openweathermap.org/data/2.5/weather?id=1264733&appid=a72702debe3ebc2f16c3357591cb131e&units=metric').json()
#     current_temperature = temp_api['main']['temp']
#     feels_like_temperature = temp_api['main']['feels_like']
#     return [current_temperature,feels_like_temperature]

def temperature(update, context):
    if(is_allowed(update)):
        current_temperature,feels_like_temperature = Commands.get_current_temperature()
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, reply_to_message_id=update.message.message_id, text=f'Current temperature in Lucknow is {current_temperature}°C. It feels like {feels_like_temperature}°C')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
        
def info(update, context):
    if(is_allowed(update)):
        try:
            sender = update.message.reply_to_message.from_user
            sender_id = sender.id
            is_sender_bot = sender.is_bot
            sender_first_name = sender.first_name
            sender_last_name = sender.last_name if sender.last_name is not None else ''
            sender_username  = sender.username if sender.username is not None else ''
            context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, 
                                     text=f'<b>User ID</b>: {sender_id}\n<b>Is User Bot</b>: {is_sender_bot}\n<b>User First Name</b>: {sender_first_name}\n<b>User Last Name</b>: {sender_last_name}\n<b>User username</b>: @{sender_username}', 
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
                        parse_mode="markdown",
                        text=f"F**k you all!")
        chat_id=update.message.chat_id
        context.bot.leave_chat(chat_id)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id, text='Who the f**k are you? You are not authorized.')
        
def main():
    updater = Updater(os.environ["BOT_TOKEN"])
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('eth',eth)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('bop',bop)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('ping',ping)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('countdown',countdown)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('stark',stark)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('temp',temperature)) #,CustomFilters.authorized_user))
    dp.add_handler(CommandHandler('info',info))
    dp.add_handler(CommandHandler('leave',leave))
#     dp.add_handler(MessageHandler(Filters.text, message_received)) #,CustomFilters.authorized_user))
#     dp.add_handler(MessageHandler(Filters.text, echo))
#     dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
