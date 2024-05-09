from django.core.management import BaseCommand

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import environ
from bot.utils import generate_code
from django.core.cache import cache



env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env('.env')

TOKEN = env.str('TOKEN')

bot = telebot.TeleBot(token=TOKEN)


def get_contact_button():
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    contact = KeyboardButton(text='Kontaktni yuborish', request_contact=True)
    button.add(contact)
    return button


@bot.message_handler(commands=['start', 'login'])
def send_welcome(message):
    msg = (f"Salom Shukurali 👋\n"
           f"@dj_auth_bot'ning rasmiy botiga xush kelibsiz\n\n"
           f"⬇️ Kontaktingizni yuboring (tugmani bosib)")

    bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=get_contact_button())


@bot.message_handler(content_types=["contact"])
def check_contact(message):
    if message.from_user.id == message.contact.user_id:
        code = generate_code()
        user_id = message.from_user.id
        cache.set(code, user_id, timeout=60)
        msg = (f"🔒 Kodingiz: \n"
               f"{code}")
        bot.send_message(message.chat.id, text=msg, reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.chat.id, text="🔑 Yangi kod olish uchun /login ni bosing")

    else:
        bot.send_message(message.chat.id, text="Shahsiy kontaktingizni yuboring")


# 1. /start [Kontakt yuboring] +
#
# 2. Send Kontakt [Tekshirish: shahsiy yoki yo'q'] +
#
# 3. Send Kod, Kesh(cache) ga salanadi +
#
# 4. Create API, kodni olib tekshiradi va user yaratadi
#
# 5. Generate tokens(access, refresh)


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.polling()
