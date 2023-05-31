import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, TOKEN_OPENAI

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = TOKEN_OPENAI


@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    # Отправляем запрос на модель GPT-3.5 Turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Вы:"},
            {"role": "user", "content": user_input},
        ]
    )
    # Получаем ответ от модели
    answer = response.choices[0].message.content
    # Отправляем ответ пользователю
    await message.reply(answer)


if __name__ == '__main__':
    executor.start_polling(dp)