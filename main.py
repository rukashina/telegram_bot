import telebot
import random
import wikipedia, re
import sqlite3


countries = ['Абхазия', 'Албания', 'Ангола', 'Армения', 'Австралия', 'Алжир', 'Андорра', 'Аруба', 'Австрия',
             'Антигуа и Барбуда', 'Афганистан', 'Азейбарджан', 'Аргентина', 'Багамские острова', 'Белиз', 'Бермудские острова',
             'Босния и Герцеговина', 'Бруней', 'Бангладеш', 'Белоруссия', 'Болгария', 'Ботсвана', 'Буркина-фасо',
             'Барбадос', 'Бельгия', 'Боливия', 'Бразилия', 'Бурунди', 'Бахрейн', 'Бенин', 'Бонэйр', 'Бутан',
             'Вануату', 'Венесуэла', 'Ватикан', 'Великобритания', 'Вьетнам', 'Венгрия', 'Габон', 'Гана', 'Германия',
             'Греция', 'Гаити', 'Гватемала', 'Гондурас', 'Грузия', 'Гайана', 'Гвинея', 'Гонконг', 'Гамбия',
             'Гвинея-Бисау', 'Гренада', 'Дания', 'Демократическая Республика Конго', 'Джерси', 'Джибути', 'Доминика',
             'Доминикана', 'Египет', 'Замбия', 'Зимбабве', 'Израиль', 'Ирак', 'Испания', 'Индия', 'Иран', 'Италия',
             'Индонезия', 'Ирландия', 'Иордания', 'Исландия', 'Йемен', 'Кабо-Верде', 'Канада', 'Киргизия', 'Корея',
             'Кувейт', 'Казахстан', 'Катар', 'Кирибати', 'Коморские острова', 'Коста-Рика', 'Кюрасао', 'Камбоджа',
             'Кения', 'Китай', 'Конго', 'Камерун', 'Кипр', 'Колумбия', 'Куба', 'КНДР', 'Лаос', 'Ливан', 'Люксембург',
             'Латвия', 'Ливия', 'Лесото', 'Литва', 'Либерия', 'Лихтенштейн', 'Маврикий', 'Малави', 'Мальдивы',
             'Мозамбик', 'Мьянма', 'Мавритания', 'Малайзия', 'Марокко', 'Молдавия', 'Мадагаскар', 'Мали', 'Монако',
             'Македония', 'Мальта', 'Мексика', 'Монголия', 'Намибия', 'Нигерия', 'Норвегия', 'Науру', 'Нидерланды',
             'Непал', 'Никарагуа', 'Нигер', 'Новая Зеландия', 'ОАЭ', 'Оман', 'Пакистан', 'Парагвай', 'Португалия',
             'Палау', 'Перу', 'Панама', 'Пуэрто-Рико', 'Папуа-Новая Гвинея', 'Польша', 'Россия', 'Руанда', 'Румыния',
             'Саба', 'Сенегал', 'Сан-Томе и Принсипи', 'Сен-Мартен', 'Сирия', 'Соломоновы острова', 'Сьерра-Леоне',
             'Сальвадор', 'Саудовская Аравия', 'Сент-Винсент и Гренадины', 'Сербия', 'Словакия', 'Сомали', 'Самоа',
             'Свазиленд', 'Сент-Китс и Невис', 'Сингапур', 'Словения', 'Судан', 'Сан-Марино', 'Сейшелы', 'Сент-Люсия',
             'Синт-Эстатиус', 'США', 'Суринам', 'Таджикистан', 'Токелау', 'Тунис', 'Таиланд', 'Тонга', 'Туркменистан',
             'Танзания', 'Тринидад и Тобаго', 'Турция', 'Того', 'Тувалу', 'Уганда', 'Уругвай', 'Узбекистан', 'Украина',
             'Уоллис и Футуна', 'Фарерские острова', 'Финляндия', 'Фиджи', 'Франция', 'Филиппины', 'Полинезия',
             'Хорватия', 'ЦАР', 'ЧАД', 'Черногория', 'Чехия', 'Чили', 'Швейцария', 'Швеция', 'Шри-Ланка', 'Эквадор',
             'Эфиопия', 'Эритрея', 'Эстония', 'ЮАР', 'Южный Судан', 'Ямайка', 'Япония']
countries_are_done = []
countries_lower = []
for c in countries:
    countries_lower.append(c.lower())

wikipedia.set_lang("ru")


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


bot = telebot.TeleBot('6170584232:AAHSEAblHQd4_Nryo9LZEU4na99zw2VBnIw')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    global countries_are_done
    countries_are_done = []
    bot.send_message(m.chat.id, 'Сыграем в игру? Напишите любую страну.\n'
                                'Чтобы узнать правила используйте команду /help\n')


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