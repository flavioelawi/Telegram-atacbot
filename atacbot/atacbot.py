import json
import telebot
import logging,time,datetime
from telebot import types
from atacbot.ataclib import ataclib
import os

configfile_path = os.path.join(os.path.expanduser("~"), ".atacbot", "config.json")
c = open(configfile_path, "r")
config = json.load(c)
telegram_key = config["telegramkey"]
bot = telebot.TeleBot(telegram_key)
logging.basicConfig(level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

def getTimestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

def put_linea(message):
    try:
        atac = ataclib()
        risposta=atac.getPercorso(message.text)
        risposta=risposta.replace("<-------",u'\U0001F68C')
        bot.send_message(message.chat.id,risposta,parse_mode="Markdown")
    except Exception as e:
        #logging.critical(risposta.text)
        logging.critical(str(e))
        bot.reply_to(message,"Linea non esistente o errore")

def put_palina(message):
    try:
        atac = ataclib()
        risposta=atac.getPalina(message.text)
        bot.send_message(message.chat.id,risposta,parse_mode="Markdown")
        #aggiungere risposta qui
    except Exception as e:
        logging.critical(str(e))
        bot.reply_to(message,"Palina non esistente o errore")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        commands={'linea' : 'Fornisce informazioni su una determinata linea','palina':"Fornisce informazioni su una fermata",'credits':"Informazioni sullo sviluppatore"}
        cid = message.chat.id
        help_text = "Sono disponibili i seguenti comandi: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page
    except:
        bot.reply_to(message,"Errore interno")

@bot.message_handler(commands=['credits'])
def credits(message):
    st = getTimestamp()
    try:
        credit = "Bot creato da Flavio Elawi, utilizzatore mezzi Atac\n"
        credit += "https://github.com/flavioelawi/Telegram-atacbot\n"
        logging.info(st + ' ' + message.from_user.username + ' ' + message.text)
        bot.send_message(message.chat.id, credit)
    except:
        bot.reply_to(message, "Errore interno")

@bot.message_handler(commands=['linea'])
def get_linea(message):
    st=getTimestamp()
    try:
        logging.info(st + ' ' + message.from_user.username  + ' ' + message.text)
        markup = types.ForceReply(selective=False)
        linea = bot.reply_to(message, "Inserisci la linea da controllare:", reply_markup=markup)
        bot.register_next_step_handler(linea, put_linea)
    except:
        bot.reply_to(message, "Errore interno")


@bot.message_handler(commands=['palina'])
def get_palina(message):
    st=getTimestamp()
    try:
        logging.info(st + ' ' + message.from_user.username  + ' ' + message.text)
        markup = types.ForceReply(selective=False)
        linea = bot.reply_to(message, "Inserisci la palina da controllare:", reply_markup=markup)
        bot.register_next_step_handler(linea, put_palina)
    except:
        bot.reply_to(message, "Errore interno")

def start():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    start()