import telebot
import datetime
import time
import threading
import random

# Вставьте свой токен здесь
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot("Здесь надо вставить свой токен")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет! Я чат бот, который будет напоминать тебе пить водичку!')
    # Запуск потока для напоминаний
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()


# Обработчик команды /fact
@bot.message_handler(commands=['fact'])
def fact_message(message):
    list = ["Вода на Земле может быть старше самой Солнечной системы: Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
        "Горячая вода замерзает быстрее холодной: Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
        "Больше воды в атмосфере, чем во всех реках мира: Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых."]
    random_fact = random.choice(list)
    bot.reply_to(message, f'Лови факт о воде: {random_fact}')


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "Я могу помочь тебе с следующими командами:\n"
        "/start - Начать общение с ботом\n"
        "/fact - Получить интересный факт о воде\n"
        "/next_water - Показать оставшееся время до следующего приема воды\n"
        "/help - Показать это сообщение\n"
        "Я также буду напоминать тебе пить воду несколько раз в день!"
    )
    bot.reply_to(message, help_text)


# Обработчик команды /next_water
@bot.message_handler(commands=['next_water'])
def next_water_message(message):
    now = datetime.datetime.now().strftime("%H:%M")
    current_time = datetime.datetime.strptime(now, "%H:%M")

    # Времена приема воды
    water_times = ["09:00", "14:00", "21:35"]

    # Найти следующее время приема воды
    next_time = None
    for time_str in water_times:
        water_time = datetime.datetime.strptime(time_str, "%H:%M")
        if current_time < water_time:
            next_time = water_time
            break

    # Если все времена прошли, берем первое время на следующий день
    if not next_time:
        next_time = datetime.datetime.strptime(water_times[0], "%H:%M") + datetime.timedelta(days=1)

    # Вычислить оставшееся время
    time_to_next_water = next_time - current_time
    hours, remainder = divmod(time_to_next_water.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    bot.reply_to(message, f'Оставшееся время до следующего приема воды: {hours} часов {minutes} минут')


# Функция для отправки напоминаний
def send_reminders(chat_id):
    first_rem = "09:00"
    second_rem = "14:00"
    end_rem = "21:35"

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == first_rem or now == second_rem or now == end_rem:
            bot.send_message(chat_id, "Напоминание - выпей стакан воды")
            time.sleep(61)  # Ожидание 61 секунды, чтобы избежать повторных отправок
        time.sleep(1)  # Задержка 1 секунда перед следующей проверкой времени


# Запуск бота
bot.polling(none_stop=True)