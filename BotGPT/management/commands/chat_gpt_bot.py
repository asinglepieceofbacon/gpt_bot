import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .config import TOKEN, TOKEN_OPENAI
from django.core.management.base import BaseCommand
from django.conf import settings

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = TOKEN_OPENAI

dialog = []


class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(self, *args, **options):
        executor.start_polling(dp)


@dp.message_handler()
async def handle_message(message: types.Message):
    global dialog
    user_input = message.text
    dialog.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "you should speak sarcastically while still giving the right answer"},
            *dialog
        ]
    )

    answer = response.choices[0].message.content
    dialog.append({"role": "assistant", "content": answer})
    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
