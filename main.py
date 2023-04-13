import telebot
import random
import wikipedia
import re
import sqlite3
from telebot import types

text = open("words/sities.txt")
countries = []
for i in text:
    countries.append(i)

for i in range(len(countries)):
    if countries[i][-1] == "\n":
        countries[i] = countries[i][:-1]

countries_are_done = []
countries_lower = []
for c in countries:
    countries_lower.append(c.lower())

wikipedia.set_lang("ru")


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        text=ny.content[:1000]
        wiki=text.split('.')
        wiki = wiki[:-1]
        wikitext = ''
        for x in wiki:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext=wikitext+x+'.'
            else:
                break
        wikitext=re.sub('\([^()]*\)', '', wikitext)
        wikitext=re.sub('\([^()]*\)', '', wikitext)
        wikitext=re.sub('\{[^\{\}]*\}', '', wikitext)
        return wikitext
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


bot = telebot.TeleBot('6170584232:AAHSEAblHQd4_Nryo9LZEU4na99zw2VBnIw')
game_is_start = False


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Игра в страны")
    item2 = types.KeyboardButton("В разработке")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id, 'Привет! Я бот-"игра в города"!\nЧем могу помочь?', reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(m, res=False):
    bot.send_message(m.chat.id, 'Пишите страну, начинающуюся на букву, на которую заканчивается предыдущее слово\n'
                                'Слова не должны повторяться\n'
                                'Если хотите узнать о стране, что я назвал, используйте команду /wiki\n'
                                'Чтобы узнать краткие сведения нажмите /info')


@bot.message_handler(commands=["wiki"])
def wiki(m, res=False):
    bot.send_message(m.chat.id, getwiki(countries_are_done[-1]))


@bot.message_handler(commands=["info"])
def info(m, res=False):
    con = sqlite3.connect("countries.db")
    cur = con.cursor()
    n = countries_lower.index(countries_are_done[-1]) + 1
    result = cur.execute("""SELECT
        country.id,
        country.name,
        country.capital,
        country.square,
        country.population,
        continents.continent
    FROM
        country
    LEFT JOIN continents
        ON continents.id = country.id_continent
    WHERE country.id = ?""", (n,)).fetchall()

    for elem in result:
        information = list(elem)

    result = f'Страна: {information[1]}\n' \
             f'Столица: {information[2]}\n' \
             f'Площадь: {information[3]} км²\n' \
             f'Численность населеня: {information[4]} чел.\n' \
             f'Материк: {information[5]}\n'
    con.close()
    bot.send_message(m.chat.id, result)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global countries_are_done
    if message.text == 'Игра в страны':
        countries_are_done = []
        bot.send_message(message.chat.id, 'Сыграем в игру? Напишите любую страну.\n'
                                      'Чтобы узнать правила используйте команду /help\n')
    else:
        country = (message.text).lower()
        maybe_countries = []
        if countries_are_done:
            last_country = countries_are_done[-1]
            if not (country in countries_lower):
                bot.send_message(message.chat.id, 'Извините, я не знаю такой страны')
            elif country in countries_are_done:
                bot.send_message(message.chat.id, 'Эта страна уже была')
            elif country[0] != last_country[-1]:
                bot.send_message(message.chat.id, 'Эта страна не подходит\n'
                                              'Нажмите /help, чтобы прочитать правила')
            else:
                countries_are_done.append(country)
                for c in countries:
                    if (c[0].lower() == country[-1]) and (not (c.lower() in countries_are_done)):
                        maybe_countries.append(c)
                if maybe_countries:
                    c = random.choice(maybe_countries)
                    bot.send_message(message.chat.id, c)
                    countries_are_done.append(c.lower())
                else:
                    bot.send_message(message.chat.id, 'Вы победили!\n'
                                                  'Я не знаю больше слов')
        else:
            if not (country in countries_lower):
                bot.send_message(message.chat.id, 'Извините, я не знаю такой страны')
            else:
                countries_are_done.append(country)
                for c in countries:
                    if (c[0].lower() == country[-1]) and (not (c.lower() in countries_are_done)):
                        maybe_countries.append(c)
                if maybe_countries:
                    c = random.choice(maybe_countries)
                    bot.send_message(message.chat.id, c)
                    countries_are_done.append(c.lower())
                else:
                    bot.send_message(message.chat.id, 'Вы победили!\n'
                                                  'Я не знаю больше слов')


bot.polling(none_stop=True, interval=0)