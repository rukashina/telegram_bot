import telebot
import random
import wikipedia
import re
import sqlite3
from telebot import types
from fuzzywuzzy import fuzz
from random import choice

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
            mayby = answer(city)
            return f'Извините, я не знаю такого города\nВозможно вы имели ввиду "{mayby.capitalize()}"?'
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
            mayby = answer(city)
            return f'Извините, я не знаю такого города\nВозможно вы имели ввиду "{mayby.capitalize()}"?'
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
            mayby = answer(country)
            return f'Извините, я не знаю такой страны\nВозможно вы имели ввиду "{mayby.capitalize()}"?'
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
            mayby = answer(country)
            return f'Извините, я не знаю такой страны\nВозможно вы имели ввиду "{mayby.capitalize()}"?'
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


def answer(text):
    try:
        a = 0
        n = 0
        nn = 0
        if now_game == 'co':
            for q in countries:
                aa=(fuzz.token_sort_ratio(q, text))
                if(aa > a and aa!= a):
                    a = aa
                    nn = n
                n = n + 1
            s = countries[nn]
        else:
            for q in cities:
                aa=(fuzz.token_sort_ratio(q, text))
                if(aa > a and aa!= a):
                    a = aa
                    nn = n
                n = n + 1
            s = cities[nn]
        return s

    except:
        return 'Ошибка'


def text_materic(a):
    con = sqlite3.connect("countries.db")
    cur = con.cursor()

    result = cur.execute("""SELECT
                continents.continent
            FROM
                country
            LEFT JOIN continents
                ON continents.id = country.id_continent
            WHERE country.name = ?""", (a,)).fetchall()
    for elem in result:
        information = list(elem)
    con.close()

    return information[0]


def text_capital(a):
    con = sqlite3.connect("countries.db")
    cur = con.cursor()

    result = cur.execute("""SELECT
                capital
            FROM
                country
            WHERE name = ?""", (a,)).fetchall()
    for elem in result:
        information = list(elem)
    con.close()

    return information[0]


bot = telebot.TeleBot('5763117043:AAGWT7DCJKQsHbrPDnE_sEJMO39us1_Sj9A')
game_is_start = False
now_game = ''
now = ''
word = ''


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global now_game
    global now
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Игра")
    item2 = types.KeyboardButton("Тест")
    markup.add(item1)
    markup.add(item2)
    now_game = ''
    now = ''
    bot.send_message(m.chat.id, 'Привет! Я бот - "страны и города"!\nЧем могу помочь?', reply_markup=markup)


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
        bot.send_message(m.chat.id, 'Извините, эта функция сейчас не доступна')


@bot.message_handler(commands=["wiki"])
def wiki(m, res=False):
    if now_game == 'co':
        bot.send_message(m.chat.id, getwiki(countries_are_done[-1]))
    elif now_game == 'ci':
        bot.send_message(m.chat.id, getwiki(cities_are_done[-1]))
    else:
        bot.send_message(m.chat.id, 'Извините, эта функция сейчас не доступна')


@bot.message_handler(commands=["info"])
def info(m, res=False):
    if now_game == 'co':
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
    else:
        bot.send_message(m.chat.id, 'Извините, эта функция сейчас не доступна')


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global countries_are_done
    global cities_are_done
    global now_game
    global now
    global word

    if message.text == 'Игра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Игра в страны")
        item2 = types.KeyboardButton("Игра в города")
        item3 = types.KeyboardButton("Назад")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        now_game = ''
        bot.send_message(message.chat.id, 'Выберите игру', reply_markup=markup)
    elif message.text == 'Тест':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Столицы")
        item2 = types.KeyboardButton("На каком материке?")
        item3 = types.KeyboardButton("Назад")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        now = ''
        bot.send_message(message.chat.id, 'Выберите тест', reply_markup=markup)

    elif message.text == 'Игра в страны':
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

    elif message.text == 'Столицы':
        now = 'ca'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Я пишу страну, а вы её столицу',
                         reply_markup=markup)
        word = choice(countries)
        bot.send_message(message.chat.id, word)

    elif message.text == 'На каком материке?':
        now = 'ma'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Я пишу страну, а вы континент, на котором она находится',
                         reply_markup=markup)
        word = choice(countries)
        bot.send_message(message.chat.id, word)

    elif message.text == 'Назад':
        if now_game:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Игра в страны")
            item2 = types.KeyboardButton("Игра в города")
            item3 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            now_game = ''
            bot.send_message(message.chat.id, 'Выберите игру', reply_markup=markup)
        elif now:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Столицы")
            item2 = types.KeyboardButton("На каком материке?")
            item3 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            now = ''
            bot.send_message(message.chat.id, 'Выберите тест', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Игра")
            item2 = types.KeyboardButton("Тест")
            markup.add(item1)
            markup.add(item2)
            now_game = ''
            now = ''
            bot.send_message(message.chat.id, 'Привет! Я бот - "страны и города"!\nЧем могу помочь?', reply_markup=markup)

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
    elif now == 'ca':
        if message.text.lower() == text_capital(word).lower():
            bot.send_message(message.chat.id, 'Да, всё верно!')
        else:
            bot.send_message(message.chat.id, f'Нет, правильный ответ - {text_capital(word)}')
        word = choice(countries)
        bot.send_message(message.chat.id, word)
    elif now == 'ma':
        if message.text.lower() == text_materic(word).lower():
            bot.send_message(message.chat.id, 'Да, всё верно!')
        else:
            bot.send_message(message.chat.id, f'Нет, правильный ответ - {text_materic(word)}')
        word = choice(countries)
        bot.send_message(message.chat.id, word)


bot.polling(none_stop=True, interval=0)