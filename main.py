import telebot
import random
import wikipedia
import re
import sqlite3
from telebot import types

# слова страны
text = open("data/words/countries.txt")
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

# города
text = open("data/words/cities.txt")
cities = []
for i in text:
    cities.append(i)

for i in range(len(cities)):
    if cities[i][-1] == "\n":
        cities[i] = cities[i][:-1]

cities_are_done = []
cities_lower = []
for c in cities:
    cities_lower.append(c.lower())

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


def need():
    global cities_are_done
    global countries_are_done
    cities_are_done = []
    countries_are_done = []


def game_cities(m):
    city = m.lower()
    maybe_cities = []
    if cities_are_done:
        last_cities = cities_are_done[-1]
        if not (city in cities_lower):
            return 'Извините, я не знаю такого города'
        elif city in cities_are_done:
            return 'Этот город уже был'
        elif city[0] != last_cities[-1]:
            return 'Этот город не подходит\nНажмите /help, чтобы прочитать правила'
        else:
            cities_are_done.append(city)
            for c in cities:
                if (c[0].lower() == city[-1]) and (not (c.lower() in cities_are_done)):
                    maybe_cities.append(c)
            if maybe_cities:
                c = random.choice(maybe_cities)
                cities_are_done.append(c.lower())
                return c
            else:
                need()
                return 'Вы победили!\nЯ не знаю больше слов\nНачинаем сначала!'
    else:
        if not (city in cities_lower):
            return 'Извините, я не знаю такой страны'
        else:
            cities_are_done.append(city)
            for c in cities:
                if (c[0].lower() == city[-1]) and (not (c.lower() in cities_are_done)):
                    maybe_cities.append(c)
            if maybe_cities:
                c = random.choice(maybe_cities)
                cities_are_done.append(c.lower())
                return c
            else:
                need()
                return 'Вы победили!\nЯ не знаю больше слов\nНачинаем сначала!'


def game_countries(m):
    country = m.lower()
    maybe_countries = []
    if countries_are_done:
        last_country = countries_are_done[-1]
        if not (country in countries_lower):
            return 'Извините, я не знаю такой страны'
        elif country in countries_are_done:
            return 'Эта страна уже была'
        elif country[0] != last_country[-1]:
            return 'Эта страна не подходит\nНажмите /help, чтобы прочитать правила'
        else:
            countries_are_done.append(country)
            for c in countries:
                if (c[0].lower() == country[-1]) and (not (c.lower() in countries_are_done)):
                    maybe_countries.append(c)
            if maybe_countries:
                c = random.choice(maybe_countries)
                countries_are_done.append(c.lower())
                return c
            else:
                need()
                return 'Вы победили!\nЯ не знаю больше слов\nНачинаем сначала!'
    else:
        if not (country in countries_lower):
            return 'Извините, я не знаю такой страны'
        else:
            countries_are_done.append(country)
            for c in countries:
                if (c[0].lower() == country[-1]) and (not (c.lower() in countries_are_done)):
                    maybe_countries.append(c)
            if maybe_countries:
                c = random.choice(maybe_countries)
                countries_are_done.append(c.lower())
                return c
            else:
                need()
                return 'Вы победили!\nЯ не знаю больше слов\nНачинаем сначала!'


bot = telebot.TeleBot('6170584232:AAHSEAblHQd4_Nryo9LZEU4na99zw2VBnIw')
game_is_start = False
now_game = ''


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global now_game
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Игра в страны")
    item2 = types.KeyboardButton("Игра в города")
    markup.add(item1)
    markup.add(item2)
    now_game = ''
    bot.send_message(m.chat.id, 'Привет! Я бот-"игра в города"!\nЧем могу помочь?', reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(m, res=False):
    if now_game == 'co':
        bot.send_message(m.chat.id, 'Пишите страну, начинающуюся на букву, на которую заканчивается предыдущее слово\n'
                                'Слова не должны повторяться\n'
                                'Если хотите узнать о стране, что я назвал, используйте команду /wiki\n'
                                'Чтобы узнать краткие сведения нажмите /info')
    elif now_game == 'ci':
        bot.send_message(m.chat.id, 'Пишите город России, начинающийся на букву, на которую заканчивается предыдущее слово\n'
                                'Слова не должны повторяться\n'
                                'Если хотите узнать о городе, что я назвал, используйте команду /wiki\n'
                                'Чтобы узнать краткие сведения нажмите /info')
    else:
        bot.send_message(m.chat.id, 'Я пока ничем не могу вам помочь!')


@bot.message_handler(commands=["wiki"])
def wiki(m, res=False):
    bot.send_message(m.chat.id, getwiki(countries_are_done[-1]))


@bot.message_handler(commands=["info"])
def info(m, res=False):
    try:
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
    except Exception as e:
        bot.send_message(m.chat.id, 'У меня нет информации об этом')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global countries_are_done
    global cities_are_done
    global now_game
    if message.text == 'Игра в страны':
        now_game = 'co'
        countries_are_done = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        item2 = types.KeyboardButton("Сброс")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Сыграем в игру? Напишите любую страну.\n'
                                      'Чтобы узнать правила используйте команду /help\n',
                         reply_markup=markup)

    elif message.text == 'Игра в города':
        now_game = 'ci'
        cities_are_done = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        item2 = types.KeyboardButton("Сброс")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Сыграем в игру? Напишите любой город.\n'
                                      'Чтобы узнать правила используйте команду /help\n',
                         reply_markup=markup)

    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Игра в страны")
        item2 = types.KeyboardButton("Игра в города")
        markup.add(item1)
        markup.add(item2)
        now_game = ''
        bot.send_message(message.chat.id, 'Привет! Я бот-"игра в города"!\nЧем могу помочь?', reply_markup=markup)

    elif message.text == 'Сброс':
        cities_are_done = []
        countries_are_done = []
        bot.send_message(message.chat.id, 'Начинаем сначала!')

    elif now_game == 'co':
        answer = game_countries(message.text)
        bot.send_message(message.chat.id, answer)
    elif now_game == 'ci':
        answer = game_cities(message.text)
        bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True, interval=0)