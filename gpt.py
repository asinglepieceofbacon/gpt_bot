from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from random import randint

from config import TOKEN, TOKEN_OPENAI

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

win = 0
num1 = 0
num2 = 0

button_hi = KeyboardButton('Привет!')
button_durak = KeyboardButton('ты дурак')
repl_markup1 = ReplyKeyboardMarkup()
repl_markup1.add(button_hi, button_durak)


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    await message.reply('Ку', reply_markup=repl_markup1)


@dp.message_handler(commands='game')
async def game_bot(message: types.Message):
    global num1, num2, correct_number

    num1 = randint(1, 100)
    num2 = randint(1, 100)
    correct_number = randint(1, 100)

    b_1 = KeyboardButton(f'{num1}')
    b_2 = KeyboardButton(f'{num2}')
    b_3 = KeyboardButton(f'{correct_number}')
    repl_markup2 = ReplyKeyboardMarkup()

    repl_markup2.add(b_1, b_2, b_3)

    await message.reply('Угадай число', reply_markup=repl_markup2)


@dp.message_handler(commands='inline')
async def inline_bot(message: types.Message):
    inline_btn1 = InlineKeyboardButton('Первая кнопка', callback_data='button1')
    inline_btn2 = InlineKeyboardButton('Вторая кнопка', callback_data='button2')
    inline_mrk = InlineKeyboardMarkup().add(inline_btn1, inline_btn2)

    await message.answer('Изначальное сообщение', reply_markup=inline_mrk)


@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_btn1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка')


@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_btn2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата вторая кнопка')


# @dp.message_handler(content_types='text')
# async def echo_bot(message: types.Message):
#     if message.text.lower() == 'ты дурак':
#         await message.answer('сам дурак!')
#     elif message.text.lower() == 'привет!':
#         await message.answer('как дела?')
#     else:
#         await message.answer(message.text)

@dp.message_handler(content_types='text')
async def game2_bot(message: types.Message):
    global correct_number
    global num1
    global num2

    if message.text.lower() == str(correct_number):
        await message.answer('Угадал')
    elif message.text.lower() != str(correct_number):
        await message.answer('Не правильно')


if __name__ == '__main__':
    executor.start_polling(dp)
