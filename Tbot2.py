# -*- coding: utf-8 -*-
import pandas as pd
import joblib
import telebot
from telebot import types
import pandas as pd
import joblib


bot = telebot.TeleBot('7194291050:AAF-_DOJHT128KrZzJUn6TPh8KAdfj_k824')

model = joblib.load('TModel.pkl')

df = pd.read_csv('Tdata.csv')
# Список станций метро
valid_stations = [
   
    'филёвский парк', 'проспект мира', 'рязанский проспект',
    'профсоюзная', 'ботанический сад', 'панфиловская', 'беломорская',
    'цветной бульвар', 'парк победы', 'багратионовская',
    'нагатинский затон', 'крылатское', 'щукинская', 'цска',
    'библиотека и ленина', 'марьина роща', 'баррикадная', 'боровицкая',
    'добрынинская', 'маяковская', 'новослободская', 'чистые пруды',
    'таганская', 'шаболовская', 'балтийская', 'мнёвники',
    'кутузовская', 'тульская', 'хорошёво', 'тургеневская',
    'новаторская', 'зил', 'международная', 'менделеевская',
    'автозаводская', 'коммунарка', 'университет', 'кантемировская',
    'полежаевская', 'театральная', 'проспект вернадского', 'калужская',
    'академическая', 'александровский сад', 'октябрьское поле',
    'коломенская', 'бульвар дмитрия донского', 'спартак', 'сокол',
    'матвеевская', 'стрешнево', 'речной вокзал', 'водный стадион',
    'нагорная', 'кузнецкий мост', 'войковская', 'новые черёмушки',
    'сретенский бульвар', 'дмитровская', 'ленинский проспект',
    'пролетарская', 'стахановская', 'аэропорт внуково',
    'выставочный центр', 'свиблово', 'ясенево', 'тимирязевская',
    'щёлковская', 'солнцево', 'зябликово', 'новопеределкино',
    'карамышевская', 'рижская', 'угрешская', 'локомотив', 'пражская',
    'рассказовка', 'гражданская', 'подольск', 'перерва', 'сокольники',
    'царицыно', 'бунинская аллея', 'улица старокачаловская',
    'черкизовская', 'ольховая', 'калитники', 'курьяново',
    'бульвар адмирала ушакова', 'первомайская', 'хорошёвская',
    'юго-западная', 'ховрино', 'физтех', 'бескудниково', 'москворечье',
    'волжская', 'электрозаводская', 'говорово', 'медведково',
    'савёловская', 'мичуринский проспект', 'владыкино', 'тропарёво',
    'чкаловская', 'красный балтиец', 'зюзино', 'сухаревская', 'окская',
    'красносельская', 'нижегородская', 'андроновка', 'семёновская',
    'зеленоград — крюково', 'озёрная', 'бутырская', 'некрасовка',
    'коптево', 'римская', 'лихоборы', 'кузьминки',
    'улица скобелевская', 'выхино', 'нахимовский проспект', 'бутово',
    'авиамоторная', 'южная', 'силикатная', 'внуково', 'трикотажная',
    'тёплый стан', 'лесопарковая', 'братиславская',
    'шоссе энтузиастов', 'улица горчакова', 'москва-товарная',
    'алтуфьево', 'новокосино', 'новохохловская',
    'улица академика янгеля', 'чертановская', 'коньково',
    'красногвардейская', 'орехово', 'пыхтино', 'остафьево',
    'бабушкинская', 'юго-восточная', 'люблино', 'новодачная',
    'алма-атинская', 'планерная', 'зорге', 'верхние лихоборы',
    'фонвизинская', 'крымская', 'красный строитель', 'севастопольская'
]


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_predict = types.KeyboardButton('/predict')
    button_help = types.KeyboardButton('/help')
    button_feedback = types.KeyboardButton('/feedback')
    markup.add(button_predict, button_help, button_feedback)

    bot.send_message(message.chat.id, """ТелеграмБот для предсказания цен

Для предсказания нажмите или введите /predict. 

Для получения дополнительной информации нажмите или введите /help.

Чтобы оставить отзыв, нажмите или введите /feedback""", reply_markup=markup)


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, """
*Инструкция *

*Начало работы*
Для начала работы с ботом отправьте команду /start.

*Предсказание стоимости*
Чтобы предсказать стоимость квартиры, отправьте команду /predict.

*Инструкции*
Чтобы получить инструкцию по использованию бота, отправьте команду /help.

*Информация о проекте*
Если вас интересует информация о проекте, отправьте команду /about.
""", parse_mode="Markdown")


@bot.message_handler(commands=['about'])
def handle_about(message):
    bot.send_message(message.chat.id, """ 
Этот бот помогает предсказать стоимость квартиры.
Для  отзыва - нажмите /feedback""")


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_message(message.chat.id, "Диалог завершен.")


feedback_df = pd.DataFrame(columns=["Отзывы"])


@bot.message_handler(commands=['feedback'])
def handle_feedback_start(message):
    bot.send_message(message.chat.id, "Оставьте, пожалуйста, отзыв:")
    bot.register_next_step_handler(message, get_feedback)


def get_feedback(message):
    user_feedback = message.text
    if user_feedback.lower() == "/stop":
        handle_stop(message)
        return

    feedback_df.loc[len(feedback_df)] = [user_feedback]
    feedback_df.to_csv('МненияЛюдей.csv', index=False)
    bot.send_message(message.chat.id, "Спасибо за ваш отзыв")


user_responses = []


@bot.message_handler(commands=['predict'])
def handle_predict_start(message):
    user_responses.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Вторичное")
    button2 = types.KeyboardButton("Новостройка")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите тип квартиры:", reply_markup=markup)
    bot.register_next_step_handler(message, get_apartment_type)


def get_apartment_type(message):
    user_response = message.text
    if user_response.lower() == "/stop":
        handle_stop(message)
        return
    if user_response not in ["Вторичное", "Новостройка"]:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_apartment_type)
        return

    user_responses.append(user_response)
    bot.send_message(message.chat.id, "Введите площадь квартиры:")
    bot.register_next_step_handler(message, get_area)


def get_area(message):
    user_response = message.text
    if user_response.lower() == "/stop":
        handle_stop(message)
        return
    try:
        area = float(user_response)
        user_responses.append(area)
    except ValueError:
        bot.send_message(message.chat.id, "Нужно ввести число")
        bot.register_next_step_handler(message, get_area)
        return

    bot.send_message(message.chat.id, "Введите количество минут до метро:")
    bot.register_next_step_handler(message, get_metro_min)


def get_metro_min(message):
    user_response = message.text
    if user_response.lower() == "/stop":
        handle_stop(message)
        return
    try:
        min = float(user_response)
        user_responses.append(min)
    except ValueError:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_metro_min)
        return

    bot.send_message(message.chat.id, "Введите станцию метро:")
    bot.register_next_step_handler(message, get_metro_station)


def get_metro_station(message):
    user_response = message.text.lower()
    if user_response.lower() == "/stop":
        handle_stop(message)
        return
    if user_response not in valid_stations:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_metro_station)
        return

    user_responses.append(user_response)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Москва")
    markup.add(button1)

    bot.send_message(message.chat.id, "Выберете регион:", reply_markup=markup)
    bot.register_next_step_handler(message, get_region)


def get_region(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    if user_response not in ["Москва"]:
        bot.send_message(message.chat.id, "Выберите  из предложенного варианта.")
        bot.register_next_step_handler(message, get_region)
        return

    user_responses.append(user_response)

    bot.send_message(message.chat.id, "Введите количество комнат:")
    bot.register_next_step_handler(message, get_room)


def get_room(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    try:
        room = float(user_response)
        user_responses.append(room)
    except ValueError:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_room)
        return

    bot.send_message(message.chat.id, "Введите площадь кухни:")
    bot.register_next_step_handler(message, get_kitchen)


def get_kitchen(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    try:
        kitchen = float(user_response)
        user_responses.append(kitchen)
    except ValueError:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_kitchen)
        return

    # Этаж
    bot.send_message(message.chat.id, "Введите этаж квартиры:")
    bot.register_next_step_handler(message, get_floor)

def get_floor(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    try:
        floor = float(user_response)
        user_responses.append(floor)
    except ValueError:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_floor)
        return

    bot.send_message(message.chat.id, "Введите этажность дома:")
    bot.register_next_step_handler(message, get_floor_count)


def get_floor_count(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    try:
        floor_count = float(user_response)
        user_responses.append(floor_count)
    except ValueError:
        bot.send_message(message.chat.id, "Введите еще раз")
        bot.register_next_step_handler(message, get_floor_count)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = types.KeyboardButton("Косметический")
    button2 = types.KeyboardButton("Евроремонт")
    button3 = types.KeyboardButton("Без ремонта")
    button4 = types.KeyboardButton("Дизайнерский")
    markup.add(button1, button2, button3, button4)

    bot.send_message(message.chat.id, "Выберете тип ремонта:", reply_markup=markup)
    bot.register_next_step_handler(message, get_repair)


def get_repair(message):
    user_response = message.text

    if user_response.lower() == "/stop":
        handle_stop(message)
        return

    if user_response not in ['Косметический', 'Евроремонт', 'Дизайнерский', 'Без ремонта']:
        bot.send_message(message.chat.id, "Выберите еще раз")
        bot.register_next_step_handler(message, get_repair)
        return

    user_responses.append(user_response)
    print(user_responses)

    data = pd.DataFrame()
    data['Тип квартиры'] = [user_responses[0]]
    data['Станция метро'] = [user_responses[3]]
    data['Минут до метро'] = [user_responses[2]]
    data['Регион'] = [user_responses[4]]
    data['Количество комнат'] = [user_responses[5]]
    data['Площадь'] = [user_responses[1]]
    data['Кухня площадь'] = [user_responses[6]]
    data['Этаж'] = [user_responses[7]]
    data['Количество этажей'] = [user_responses[8]]
    data['Ремонт'] = [user_responses[9]]

    predicted_values = make_prediction(data)

    predicted_values = ', '.join(['{:,.0f}'.format(value).replace(',', ' ') for value in predicted_values])
    print(predicted_values)

    bot.send_message(message.chat.id, f"Цена квартиры: {predicted_values}")

def make_prediction(data):
    pred = model.predict(data)
    return pred

bot.infinity_polling()