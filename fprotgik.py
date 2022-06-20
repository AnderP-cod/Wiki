import wikipedia
import telebot

wikipedia.set_lang('ru')
bot = telebot.TeleBot('5563549236:AAHlMTSp_vUhCyDOYAq37YrDG3Lb9-HuSlI')


@bot.message_handler(commands=['start'])
def start_message(sta):
    bot.send_message(sta.chat.id, "Hallo")


@bot.message_handler(content_types=['text'])
def wiki_message(wiki):
    word = wiki.text.strip().lower()
    print(word)
    try:
        wiki_message_final = wikipedia.summary(word)
    except wikipedia.exceptions.PageError:
        bot.send_message(wiki.chat.id, "Ошибка")
    bot.send_message(wiki.chat.id, wiki_message_final, parse_mode='html')


bot.polling(none_stop=True)