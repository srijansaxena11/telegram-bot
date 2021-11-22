from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
import requests
import re
import logging
from uuid import uuid4
from telegram.utils.helpers import escape_markdown
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def get_eth_rate_inr():
    print("Inside get_eth_rate_inr()")
    eth_api = requests.get('https://rest.coinapi.io/v1/exchangerate/ETH/INR?apikey=95CBCBB3-72EB-48D3-B60D-9DDCB21F70AF').json()
    rate = eth_api['rate']
    return rate

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def stark(update, context):
    f = open("/etc/openhab2/scripts/tony_stark_quotes.txt","r")
    r = random.randint(0,49)
    lines = f.readlines()
    quote = lines[r]
    context.bot.send_message(chat_id=update.message.chat_id, text=quote)

def eth(update, context):
    print("Inside eth()")
    rate = get_eth_rate_inr()
    context.bot.send_message(chat_id=update.message.chat_id, text=rate)

def bop(update, context):
    url = get_url()
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=url)

def start(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello. Good Morning/Noon/Evening, whatever it is. I am Srijan sir's Virtual Assistant. I am a bot if you didn't notice. I am developed to provide information or answer queries regarding Srijan sir. I'm still in very early phase of development. So, I may answer only a few questions at the moment. Also I'm not a regular bot. I'm a part time bot. I may not respond at certain times when Srijan sir has not turned on his server. Or he may even completely shut me down if I don't seem to be useful enough to consume processing, storage and bandwidth on Srijan sir's server. ")

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def sleeping(update, context):
    print("Inside sleeping()")
#    if ((update.message.text.find("srijan") != -1) and ((update.message.text.find("sleep") != -1) or (update.message.text.find("wake") != -1) or (update.message.text.find("woke") != -1))):
#        f = open("/home/openhabian/isSleeping","r")
#        if (f.read()=="1\n"):
#            bot.send_message(chat_id=update.message.chat_id, text="Yes, Srijan sir is sleeping currently. Don't you dare to disturb him.")
#        else:
#            bot.send_message(chat_id=update.message.chat_id, text="No, Srijan sir is not sleeping currently. He may ignore you nonetheless.")
    if ((update.message.text.find("hi") != -1) or (update.message.text.find("hello") != -1)):
        context.bot.send_message(chat_id=update.message.chat_id, text="You are trying to initiate a conversation with a bot? You seriously need to find a hobby.")
    elif (update.message.text.find("bye") != -1):
        context.bot.send_message(chat_id=update.message.chat_id, text="I don't even know you.")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Either you are dumb or I am. I am bot in my initial phase and being worked upon. So fingers on you.\nP.S.: Command doesn't exist. Let @SrijanSaxena know to add the required command. ")

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

def main():
    updater = Updater('2113253226:AAHH4MMbAQieoxDQWZmpll3aJPMW6C9G4_M')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('eth',eth))
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('stark',stark))
    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, sleeping))
    dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
