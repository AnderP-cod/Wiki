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

wikipedia.set_lang('ru')
bot = telebot.TeleBot(Token.Token_telegram)
print("start protgik")


@bot.message_handler(commands=['start'])
def start_message(wiki):
    markup = types.ReplyKeyboardMarkup()
    item1 = types.KeyboardButton("Сделать поиск по википедии")
    item2 = types.KeyboardButton("Рандомная стать с википедии")
    markup.add(item1, item2)
    bot.send_message(wiki.chat.id, "Здравствуйте, что вы хотите сделать", reply_markup=markup)
    bot.register_next_step_handler(wiki, start_message_if)

@bot.message_handler(commands=['help'])
def help_message(help):
    bot.send_message(help.chat.id, "Телеграм бот умеет делать поиск по\n векипедии и находить рандомную статью в википедии")


@bot.message_handler(content_types=['text'])
def start_message_if(wiki):
    if wiki.text == "Сделать поиск по википедии":
        bot.register_next_step_handler(wiki, wiki_message)
    elif wiki.text == "Рандомная стать с википедии":
        bot.send_message(wiki.chat.id, "Нажмите 2 раза чтобы сработала функция 'Рандомная стать с википедии'")
        bot.register_next_step_handler(wiki, wiki_message_random)


def wiki_message(wiki):
    word = wiki.text
    print(word)
    search_on_wikipedia = wikipedia.page(word).content
    bot.send_message(wiki.chat.id, search_on_wikipedia, parse_mode='html')


def wiki_message_random(wiki):
    url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    url = "https://en.wikipedia.org/wiki/%s" % title
    webbrowser.open(url)


bot.polling(none_stop=True)
