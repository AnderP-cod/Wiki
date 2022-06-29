import wikipedia
import telebot
import requests
from bs4 import BeautifulSoup
import webbrowser
import random
from telebot import types
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup
import Token

wikipedia.set_lang('uk')
bot = telebot.TeleBot(Token.Token_telegram)
print("start protgik")


@bot.message_handler(commands=['start'])
def start_message(wiki):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Зробити пошук")
    item2 = types.KeyboardButton("Рандомна стаття")
    markup.add(item1, item2)
    bot.send_message(wiki.chat.id, "Доброго дня! Що ви хочете зробити", reply_markup=markup)
    bot.register_next_step_handler(wiki, start_message_if)

@bot.message_handler(commands=['help'])
def help_message(help):
    bot.send_message(help.chat.id, "Телеграм бот вміє робити пошук по\nвікипедії і знаходити рандомну статтю у вікіпедії")


@bot.message_handler(content_types=['text'])
def start_message_if(wiki):
    if wiki.text == "Зробити пошук":
        bot.send_message(wiki.chat.id, "Напишіть, що ви хочете знайти")
        bot.register_next_step_handler(wiki, wiki_message)
    elif wiki.text == "Рандомна стаття":
        bot.send_message(wiki.chat.id, "Натисніть 2 рази щоб спрацювала функція Рандомна стаття з вікіпедії")
        bot.register_next_step_handler(wiki, wiki_message_random)


def wiki_message(wiki):
    try:
        word = wiki.text.lower()
        print(word)
        search_on_wikipedia = wikipedia.summary(word)
        bot.send_message(wiki.chat.id, search_on_wikipedia, parse_mode='html')
    except Exception:
        bot.send_message(wiki.chat.id, "Телеграм бот не може знайти статтю")


def wiki_message_random(wiki):
    url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    url = "https://en.wikipedia.org/wiki/%s" % title
    bot.send_message(wiki.chat.id, url)
    webbrowser.open(url)


bot.polling(none_stop=True)
