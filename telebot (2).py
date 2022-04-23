import telebot
from telebot import types
import sqlite3
import config
import requests
import random

conn = sqlite3.connect('couchsurf.db', check_same_thread=False)
cursor = conn.cursor()

bot = telebot.TeleBot(config.token)


def db_table_val(user_id: int, user_name: str, username: str,
                 user_fio: str, user_age: int, user_address: str, user_description: str, user_status: str,
                 user_photos: str):
    result = cursor.execute("""SELECT user_id FROM information""").fetchall()
    for i in result:
        if user_id == i[0]:
            cursor.execute(f"UPDATE information SET user_name = '{user_name}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET username = '{username}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_fio = '{user_fio}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_age = '{user_age}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_address = '{user_address}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_description = '{user_description}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_status = '{user_status}' WHERE user_id = {user_id}")
            cursor.execute(f"UPDATE information SET user_photos = '{user_photos}' WHERE user_id = {user_id}")
            break
    else:
        cursor.execute('INSERT INTO information (user_id, user_name, username, user_fio, user_age,'
                       ' user_address, user_description, user_status, user_photos) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, user_name, username, user_fio, user_age, user_address, user_description,
                        user_status, user_photos))
    conn.commit()


all_inf = {}
form_slow = {}
xxx = {}
showing = {}
sss = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    global all_inf
    rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    rmk.add(types.KeyboardButton('Я Серфер'), types.KeyboardButton('Я Хост'),
            types.KeyboardButton('Подробности и правила'))

    msg = bot.send_message(message.chat.id, 'Привет, это Couchsurfing_bot. Я помогу вам найти '
                                            'бесплатное место жительство во время вашего путешествия'
                                            ' или же наоборот найти вам сожителей.'
                                            ' Выберите подходящий для вас вариант', reply_markup=rmk)
    all_inf[message.chat.id] = [[], False, '']
    all_inf[message.chat.id][0].append(message.from_user.id)
    all_inf[message.chat.id][0].append(message.from_user.first_name)
    all_inf[message.chat.id][0].append(message.from_user.username)
    bot.register_next_step_handler(msg, user_answer)


def user_answer(message):
    types.ReplyKeyboardRemove(selective=False)
    if message.text == 'Я Серфер':
        msg = bot.send_message(message.chat.id, 'Отлично, теперь давайте '
                                                'узнаем о вас по подробнее. Как вас зовут? (ФИО полность)')
        bot.register_next_step_handler(msg, user_serf_reg1)
    elif message.text == 'Я Хост':
        msg = bot.send_message(message.chat.id, 'Отлично, теперь давайте '
                                                'узнаем о вас по подробнее. Как вас зовут? (ФИО полность)')
        bot.register_next_step_handler(msg, user_host_reg1)
    elif message.text == 'Подробности и правила':
        rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        rmk.add(types.KeyboardButton('Назад'))
        msg = bot.send_message(message.chat.id,
                               '    Каучсёрфинг (буквально «поиск дивана») — ночёвка в доме незнакомого '
                               'человека, готового принимать других незнакомцев. По сути, это клуб по '
                               'интересам, гигантская гостевая социальная сеть, объединяющая'
                               ' путешественников со всего мира. \n    Каучсёрфинг — это философия и '
                               'определённый стиль путешествий. Его суть в знакомстве и общении, а не '
                               'в выгоде. Это приключение, возможность узнать другую страну через её '
                               'жителей и завести друзей по всему миру.\n\n    Host - тот, кто принимает'
                               ' в гости. \n    Серфер - путешественник. \n\n    Базовые правила: \n\n    '
                               '1. Будьте честны со своим хостом (тем, кто вас принимает) при знакомстве.'
                               ' Неважно, заполняете ли профиль на сайте каучсёрфинга или '
                               'договариваетесь с друзьями из фейсбука. Не пишите, что вы общительны и'
                               ' обожаете встречи с новыми людьми, если на самом деле вы интроверт. '
                               'Вряд ли вас обрадует вечеринка, устроенная хостом в честь вашего '
                               'приезда. \n    2. Ничего не ждите от хоста. То, что человек согласился '
                               'предоставить вам жильё, не значит, что он готов встречать гостей в '
                               'аэропорту, готовить им или организовывать их досуг. Конечно, он может '
                               'сам захотеть сделать что-то для вас. Но вовсе не обязан.\n    3. Сообщать'
                               ' своему хосту об изменившихся планах или маршруте — не просто хороший'
                               ' тон, а необходимость. Дайте человеку возможность скорректировать свои'
                               ' планы, а не просто бесцельно ждать гостей, у которых задержался рейс.'
                               '\n    4. Не останавливайтесь у одного хоста слишком долго. Оптимальное'
                               ' время — 2–3 дня. Если нужно больше, лучше остановиться у нескольких'
                               ' хозяев. Даже если едете к друзьям, подумайте, как долго они готовы '
                               'делить с кем-то свой быт. \n    5. Продлевать визит дольше '
                               'запланированного — тоже плохо. Люди часто стесняются отказать в '
                               'просьбе, но это не повод оставаться в чужом доме дольше, чем '
                               'договаривались. \n    6. Если вам предоставили место для ночлега на '
                               'длительный срок, постарайтесь заниматься своими делами и помнить, что '
                               'у хозяев есть свои дела. Например, ходите гулять почаще, особенно если'
                               ' хост работает дома. \n    7. С другой стороны, хозяева, скорее всего,'
                               ' сами захотят уделить вам время: что-то показать, куда-то сводить, '
                               'с кем-то познакомить. Даже если такой досуг не всегда совпадает с '
                               'вашими планами, отнеситесь к этому с благодарностью. Тем более, '
                               'местным есть что показать. Если это вообще не в вашем стиле, стоит '
                               'подумать об остановке в отеле. \n    8. Поделитесь с хозяином планами на '
                               'поездку и вашими предпочтениями заранее. Это поможет избежать ненужных'
                               ' усилий с обеих сторон. \n\n Возможности бота: \n\n'
                               '/start - функция запуска бота. В ней вы можете заполнить свои данные или поменять их.\n'
                               '/search - функция поиска хоста.\n/my_information - посмотреть мои данные. \n'
                               '/change_name - изменить ФИО.\n/change_age - изменить'
                               ' возраст. \n /change_address - изменить место жительства/населенный пункт, который'
                               ' собираетесь посетить. \n/change_status - изменить статус (с Host`a на Serfer`a '
                               'и наоборот). \n/change_description - изменить свое описание.'
                               '\n\nКак работает бот: \n\n1. Все пользователи регистрируються.\n'
                               '2. Серферы с помощью функции /search выбирают себе подходящий вариант среди анкет.\n'
                               '3. Бот отправляет серферу имя выбранного хоста, для дальнейшего'
                               ' обсуждения подробностей встречи', reply_markup=rmk)
        bot.register_next_step_handler(msg, start_message)


def user_serf_reg1(message):
    global all_inf
    # добавление имени
    all_inf[message.chat.id][0].append(message.text)
    msg = bot.send_message(message.chat.id, 'Сколько вам лет?')
    bot.register_next_step_handler(msg, user_serf_reg2)


def user_serf_reg2(message):
    global all_inf
    if str(message.text).isdigit():
        # ддобавление возраста
        all_inf[message.chat.id][0].append(int(message.text))
        msg = bot.send_message(message.chat.id, 'Напишите название населенного пункта, в котором вы хотите поехать?')
        bot.register_next_step_handler(msg, user_serf_reg3)
    else:
        msg = bot.send_message(message.chat.id, 'Вы вели не число.')
        bot.register_next_step_handler(msg, user_serf_reg2)


def user_serf_reg3(message):
    global all_inf
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493" \
                       f"-4b70-98ba-98533de7710b&geocode={message.text}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            if toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][0]['name'] == 'Россия' and \
                    toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1]['kind'] == 'locality':
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1]['name']
                all_inf[message.chat.id][0].append(toponym_address)
                msg = bot.send_message(message.chat.id, 'Опишите себя максимально подробно. Можете ответить на '
                                                        'контрольные вопросы: \n \t1) Чем вы занимаетесь?'
                                                        ' (учитесь или может работаете) \n \t2) Есть ли у вас хобби?'
                                                        '\n \t3) Опишите себя 3 словами. '
                                                        '\n \t4) Какого вы пола?')
                bot.register_next_step_handler(msg, user_serf_reg4)
            else:
                msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                        'или же вовсе не название населеного пункта. Повторите попытку.')
                bot.register_next_step_handler(msg, user_serf_reg3)
        except IndexError as e:
            msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                    'или же вовсе не название населеного пункта. Повторите попытку.')
            bot.register_next_step_handler(msg, user_serf_reg3)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                'или же вовсе не название населеного пункта. Повторите попытку.')
        bot.register_next_step_handler(msg, user_serf_reg3)


def user_serf_reg4(message):
    global all_inf
    all_inf[message.chat.id][0].append(message.text)
    all_inf[message.chat.id][0].append("Serfer")
    msg = bot.send_message(message.chat.id, 'Отправьте фотки самого себя (от 1 до 5 штук)')
    while not all_inf[message.chat.id][1]:
        pass
    msg = bot.send_message(message.chat.id, 'Отлично')
    bot.register_next_step_handler(msg, end_reg)


def user_host_reg1(message):
    global all_inf
    all_inf[message.chat.id][0].append(message.text)
    msg = bot.send_message(message.chat.id, 'Сколько вам лет?')
    bot.register_next_step_handler(msg, user_host_reg2)


def user_host_reg2(message):
    global all_inf
    if str(message.text).isdigit():
        all_inf[message.chat.id][0].append(int(message.text))
        msg = bot.send_message(message.chat.id, 'Напиши название населенного пункта, в котором проживаешь.')
        bot.register_next_step_handler(msg, user_host_reg3)
    else:
        msg = bot.send_message(message.chat.id, 'Вы вели не число.')
        bot.register_next_step_handler(msg, user_host_reg2)


def user_host_reg3(message):
    global all_inf
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493" \
                       f"-4b70-98ba-98533de7710b&geocode={message.text}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            if toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][0]['name'] == 'Россия' and \
                    toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1]['kind'] == 'locality':
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1]['name']
                all_inf[message.chat.id][0].append(toponym_address)
                msg = bot.send_message(message.chat.id, 'Опишите себя максимально подробно. Можете ответить на '
                                                        'контрольные вопросы: \n \t1) Чем вы занимаетесь?'
                                                        ' (учитесь или может работаете) \n \t2) Есть ли у вас хобби?'
                                                        '\n \t3) Опишите себя 3 словами. '
                                                        '\n \t4) Какого вы пола?')
                bot.register_next_step_handler(msg, user_host_reg4)
            else:
                msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                        'или же вовсе не название населеного пункта. Повторите попытку.')
                bot.register_next_step_handler(msg, user_host_reg3)
        except IndexError as e:
            msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                    'или же вовсе не название населеного пункта. Повторите попытку.')
            bot.register_next_step_handler(msg, user_host_reg3)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                'или же вовсе не название населеного пункта. Повторите попытку.')
        bot.register_next_step_handler(msg, user_host_reg3)


def user_host_reg4(message):
    global all_inf, sss
    all_inf[message.chat.id][0].append(message.text)
    all_inf[message.chat.id][0].append("Host")
    msg = bot.send_message(message.chat.id, 'Отправьте фотки дома и самого себя (от 1 до 5 штук)')
    while not all_inf[message.chat.id][1]:
        pass
    msg = bot.send_message(message.chat.id, 'Отлично')
    bot.register_next_step_handler(msg, end_reg)


def end_reg(message):
    global all_inf, sss
    all_inf[message.chat.id][0].append(sss)
    if len(all_inf[message.chat.id][0]) == 9:
        all_inf[message.chat.id][0][8] = all_inf[message.chat.id][2]
    print(all_inf)
    db_table_val(user_id=int(all_inf[message.chat.id][0][0]), user_name=all_inf[message.chat.id][0][1],
                 username=all_inf[message.chat.id][0][2], user_fio=all_inf[message.chat.id][0][3],
                 user_age=int(all_inf[message.chat.id][0][4]), user_address=all_inf[message.chat.id][0][5],
                 user_description=all_inf[message.chat.id][0][6],
                 user_status=all_inf[message.chat.id][0][7], user_photos=all_inf[message.chat.id][0][8])
    all_inf[message.chat.id] = [[], False, '']
    sss = ''


@bot.message_handler(commands=['search'])
def search(message):
    global showing
    result = cursor.execute(
        f"""SELECT user_status, user_address FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        if result[0] == 'Host':
            msg = bot.send_message(message.chat.id, 'Это функция недоступна для вас, так как у вас стоит статус "Host"')
        elif result[0] == 'Serfer':
            res1 = cursor.execute(
                f"""SELECT * FROM information where user_status = 'Host' and user_address = '{result[1]}'""").fetchall()
            print(res1)
            if res1:
                for i in res1:
                    request_url = "https://api.telegram.org/bot" + config.token + "/sendChatAction"
                    params = {
                        "chat_id": f"{i[1]}",
                        "action": "typing"
                    }
                    result1 = requests.post(request_url, params=params)
                    if 'false' in str(result1.text):
                        print(i[1])
                        cursor.execute(
                            f"DELETE from information where user_id = {i[1]}")
                        conn.commit()
                res1 = cursor.execute(
                    f"""SELECT * FROM information where user_status = 'Host'
                            and user_address = '{result[1]}'""").fetchall()
                showing[message.chat.id] = []
                msg = bot.send_message(message.chat.id, 'Вот какие мы сумели найти вариаты:')
                rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                rmk.add(types.KeyboardButton('Подходит'), types.KeyboardButton('Не подходит'))
                xxx[message.chat.id] = random.choice(res1)
                form_slow[message.chat.id] = xxx[message.chat.id][-1].split(';')[0:-1]
                for i in form_slow[message.chat.id]:
                    filess = open(f'data/{i}', 'rb')
                    bot.send_photo(message.chat.id, filess)
                msg = bot.send_message(message.chat.id, f'ФИО: {xxx[message.chat.id][4]} \n\n'
                                                        f'Возраст: {xxx[message.chat.id][5]} \n\n '
                                                        f'Населенный пункт: {xxx[message.chat.id][6]} \n\n'
                                                        f'Краткое описание: {xxx[message.chat.id][7]} \n\n',
                                       reply_markup=rmk)
                showing[message.chat.id].append(xxx[message.chat.id][1])
                bot.register_next_step_handler(msg, form)
            else:
                msg = bot.send_message(message.chat.id,
                                       'К сожалению, мы не смогли найти ни одного подходящего человека.'
                                       ' Возможно вам стоит сменить город.')
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


def form(message):
    global form_slow
    form_slow[message.chat.id] = False

    def form1(message):
        global xxx, form_slow, showing
        result = cursor.execute(
            f"""SELECT user_status, user_address FROM information where user_id = {message.chat.id}""").fetchone()
        res1 = cursor.execute(
            f"""SELECT * FROM information where user_status = 'Host' and user_address = '{result[1]}'""").fetchall()
        if message.text == 'Подходит':
            res2 = cursor.execute(
                f"""SELECT username FROM information where user_id = {showing[message.chat.id][-1]}""").fetchone()
            msg = bot.send_message(message.chat.id, f'Имя данного пользователя: \n\n@{res2[0]} \n\n '
                                                    f'Познакомтесь и обсудите все важные, дальнейшие момент с ним/ней. '
                                                    f'Удачных путешествий!')
        else:
            rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            rmk.add(types.KeyboardButton('Подходит'), types.KeyboardButton('Не подходит'))
            xxx[message.chat.id] = random.choice(res1)
            form_slow[message.chat.id] = xxx[message.chat.id][-1].split(';')[0:-1]
            for i in form_slow[message.chat.id]:
                filess = open(f'data/{i}', 'rb')
                bot.send_photo(message.chat.id, filess)
            msg = bot.send_message(message.chat.id, f'ФИО: {xxx[message.chat.id][4]} \n\n'
                                                    f'Возраст: {xxx[message.chat.id][5]} \n\n '
                                                    f'Населенный пункт: {xxx[message.chat.id][6]} \n\n'
                                                    f'Краткое описание: {xxx[message.chat.id][7]} \n\n',
                                   reply_markup=rmk)
            showing[message.chat.id].append(xxx[message.chat.id][1])
            bot.register_next_step_handler(msg, form)

    form1(message)


@bot.message_handler(commands=['change_name'])
def change_name(message):
    def chacha(message):
        cursor.execute(f"UPDATE information SET user_fio = '{message.text}' WHERE user_id = {message.chat.id}")
        msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь ваше ФИО: {message.text}')
        conn.commit()

    result = cursor.execute(
        f"""SELECT user_fio FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        msg = bot.send_message(message.chat.id, f'Ваше старое ФИО: {result[0]}\n\n Введите новое ФИО:')
        bot.register_next_step_handler(msg, chacha)
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(commands=['change_status'])
def change_status(message):
    def chacha4(message):
        if message.text == 'Да':
            cursor.execute(f"UPDATE information SET user_status = 'Serfer' WHERE user_id = {message.chat.id}")
            msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь ваш статус: "Serfer"')
            conn.commit()
        elif message.text == 'Нет':
            msg = bot.send_message(message.chat.id, f'Мы не изменили ваш статус, так как вы нажали на кнопку "Нет"')
        else:
            msg = bot.send_message(message.chat.id, f'Нажмите на кнопку "Нет" либо "Да"')
            bot.register_next_step_handler(msg, chacha4)

    def chacha5(message):
        if message.text == 'Да':
            cursor.execute(f"UPDATE information SET user_status = 'Host' WHERE user_id = {message.chat.id}")
            msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь ваш статус: "Host"')
            conn.commit()
        elif message.text == 'Нет':
            msg = bot.send_message(message.chat.id, f'Мы не изменили ваш статус, так как вы нажали на кнопку "Нет"')
        else:
            msg = bot.send_message(message.chat.id, f'Нажмите на кнопку "Нет" либо "Да"')
            bot.register_next_step_handler(msg, chacha5)

    result = cursor.execute(
        f"""SELECT user_status FROM information where user_id = {message.chat.id}""").fetchone()
    rmk = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    rmk.add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))
    if result:
        if result[0] == 'Host':
            msg = bot.send_message(message.chat.id, f'Ваш старый статус: {result[0]}\n\n Вы действительно'
                                                    f' хотите его поменять на "Serfer"', reply_markup=rmk)
            bot.register_next_step_handler(msg, chacha4)
        elif result[0] == 'Serfer':
            msg = bot.send_message(message.chat.id, f'Ваш старый статус: {result[0]}\n\n Вы действительно'
                                                    f' хотите его поменять на "Host"', reply_markup=rmk)
            bot.register_next_step_handler(msg, chacha5)
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(commands=['change_age'])
def change_age(message):
    def chacha3(message):
        if str(message.text).isdigit():
            cursor.execute(f"UPDATE information SET user_age = {int(message.text)} WHERE user_id = {message.chat.id}")
            msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь ваш возраст: {int(message.text)}')
            conn.commit()
        else:
            msg = bot.send_message(message.chat.id, 'Вы вели не число. Повторите попытку.')
            bot.register_next_step_handler(msg, chacha3)

    result = cursor.execute(
        f"""SELECT user_age FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        msg = bot.send_message(message.chat.id, f'Ваше старый возраст: {result[0]}\n\n Введите новый возраст:')
        bot.register_next_step_handler(msg, chacha3)
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(commands=['change_address'])
def change_address(message):
    def chacha1(message):
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493" \
                           f"-4b70-98ba-98533de7710b&geocode={message.text}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            try:
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                if toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][0]['name'] == 'Россия' and \
                        toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1][
                            'kind'] == 'locality':
                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1][
                        'name']
                    cursor.execute(f"UPDATE information SET user_address = '{toponym_address}' "
                                   f"WHERE user_id = {message.chat.id}")
                    msg = bot.send_message(message.chat.id, f'Изменение сохранено, '
                                                            f'теперь ваше место жительства: {toponym_address}')
                    conn.commit()
                else:
                    msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                            'или же вовсе не название населеного пункта.'
                                                            ' Повторите попытку.')
                    bot.register_next_step_handler(msg, chacha1)
            except IndexError as e:
                msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                        'или же вовсе не название населеного пункта. '
                                                        'Повторите попытку.')
                bot.register_next_step_handler(msg, chacha1)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                    'или же вовсе не название населеного пункта. Повторите попытку.')
            bot.register_next_step_handler(msg, chacha1)

    def chacha2(message):
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493" \
                           f"-4b70-98ba-98533de7710b&geocode={message.text}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            try:
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                if toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][0]['name'] == 'Россия' and \
                        toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1][
                            'kind'] == 'locality':
                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]['Components'][-1][
                        'name']
                    cursor.execute(f"UPDATE information SET user_address = '{toponym_address}'"
                                   f" WHERE user_id = {message.chat.id}")
                    msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь населенный пункт, '
                                                            f'в который вы хотите отправиться: {toponym_address}')
                    conn.commit()

                else:
                    msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                            'или же вовсе не название населеного пункта.'
                                                            ' Повторите попытку.')
                    bot.register_next_step_handler(msg, chacha2)
            except IndexError as e:
                msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                        'или же вовсе не название населеного пункта. '
                                                        'Повторите попытку.')
                bot.register_next_step_handler(msg, chacha2)
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            msg = bot.send_message(message.chat.id, 'Возможно вы вели город, находящийся не в России, '
                                                    'или же вовсе не название населеного пункта. Повторите попытку.')
            bot.register_next_step_handler(msg, chacha2)

    result = cursor.execute(
        f"""SELECT user_address, user_status FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        if result[1] == 'Host':
            msg = bot.send_message(message.chat.id, f'Ваше старое место жительства: {result[0]}\n\n Введите новое '
                                                    f'место жительства:')
            bot.register_next_step_handler(msg, chacha1)
        elif result[1] == 'Serfer':
            msg = bot.send_message(message.chat.id, f'Населенный пункт, в который вы раньше собирались отправиться:'
                                                    f' {result[0]}\n\n'
                                                    f' Введите новый населенный пункт:')
            bot.register_next_step_handler(msg, chacha2)
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(commands=['change_description'])
def change_name(message):
    def chacha6(message):
        cursor.execute(f"UPDATE information SET user_description = '{message.text}' WHERE user_id = {message.chat.id}")
        msg = bot.send_message(message.chat.id, f'Изменение сохранено, теперь ваше новое '
                                                f'описание выглядит так: {message.text}')
        conn.commit()

    result = cursor.execute(
        f"""SELECT user_description FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        msg = bot.send_message(message.chat.id, f'Ваше старое описание: {result[0]}\n\n Можете ответить на '
                                                'контрольные вопросы: \n \t1) Чем вы занимаетесь?'
                                                ' (учитесь или может работаете) \n \t2) Есть ли у вас хобби?'
                                                '\n \t3) Опишите себя 3 словами. '
                                                '\n \t4) Какого вы пола?\n\nВведите новое описание:')
        bot.register_next_step_handler(msg, chacha6)
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(commands=['my_information'])
def my_inf(message):
    result = cursor.execute(
        f"""SELECT * FROM information where user_id = {message.chat.id}""").fetchone()
    if result:
        form_slow[message.chat.id] = result[-1].split(';')[0:-1]
        for i in form_slow[message.chat.id]:
            filess = open(f'data/{i}', 'rb')
            bot.send_photo(message.chat.id, filess)
        msg = bot.send_message(message.chat.id, f'ФИО: {result[4]} \n\n'
                                                f'Возраст: {result[5]} \n\n '
                                                f'Населенный пункт: {result[6]} \n\n'
                                                f'Краткое описание: {result[7]} \n\n'
                                                f'Статус:  {result[8]} \n\n')
    else:
        msg = bot.send_message(message.chat.id, 'Сначало нужно заполнить данные. \n\nНапишите /start \n\n')


@bot.message_handler(content_types=['photo'])
def photo(message):
    try:
        global all_inf, sss
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        print(all_inf[message.chat.id], message.chat.id)
        src = r'C:\Users\Lenovo\PycharmProjects\pythonProject1\data' + '\\' + file_info.file_path.split('/')[-1]
        if 'Host' in all_inf[message.chat.id][0] or 'Serfer' in all_inf[message.chat.id][0]:
            all_inf[message.chat.id][2] += file_info.file_path.split('/')[-1] + ';'
            all_inf[message.chat.id][1] = True
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    except Exception as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True, interval=0)
