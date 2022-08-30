import telebot
from dotenv import dotenv_values
from map_num_name import NUM2NAME

# Создаем экземпляр бота
bot = telebot.TeleBot(dotenv_values(".env")["TG_BOT_TOKEN"])

audio_cache = {}


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне номер аудио )')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        if message.text in audio_cache:
            bot.send_audio(message.from_user.id, audio_cache[message.text])
        else:
            with open(r'./audio/{}'.format(NUM2NAME[message.text]), 'rb') as audio:
                audio_md = bot.send_audio(message.from_user.id, audio)
                audio_cache[message.text] = audio_md.audio.file_id
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Аудио не найдено')


# TODO: функционал добаления аудиозаписей


# Запускаем бота
bot.polling(none_stop=True, interval=0)