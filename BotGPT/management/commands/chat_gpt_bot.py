import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from .config import TOKEN, TOKEN_OPENAI
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
from django.conf import settings
from BotGPT.models import Dialog, Message

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
openai.api_key = TOKEN_OPENAI


class Command(BaseCommand):
    help = 'Telegram bot setup command'

    def handle(self, *args, **options):
        sync_to_async(executor.start_polling(dp))


@sync_to_async
def save_user_message(dialog, user_input):
    role_user = "user"
    dialog_obj, _ = Dialog.objects.get_or_create(username=f'{dialog}', role=role_user)
    user_message = Message(dialog=dialog_obj, role=role_user, content=role_user)
    user_message.save()

@sync_to_async
def save_assistant_message(dialog, user_input):
    role_assistant = "assistant"
    dialog_obj, _ = Dialog.objects.get_or_create(username=f'{dialog}', role=role_assistant)
    assistant_message = Message(dialog=dialog_obj, role=role_assistant, content=role_assistant)
    assistant_message.save()

@dp.mwssage_handler(commands=['delete_dialog'])
async def delete_dialof(message: types.Message):
    dialog_str = f'{message.from_user.username}'

    dialogs = await sync_to_async(Dialog.objects.filter)(username=dialog_str)

    dialogs = await sync_to_async(list)(dialogs)

    for dialog in dialogs:
        await sync_to_async(dialog.delete)()

    messages = await sync_to_async(Message.objects.filter)(dialog_username=dialog_str)

    messages = await sync_to_async(list)(messages)

    for message in messages:
        await sync_to_async(message.delete)()


    await message.reply('Диалог ассистентом был удалён')

@dp.message_handler()
async def handle_message(message: types.Message):
    user_input = message.text
    dialog_str = f'{message.from_user.username}'
    await save_user_message(dialog_str, user_input)

    dialog_objs = await sync_to_async(Dialog.objects.filter)(username=f'{dialog_str}')
    previous_messages = await sync_to_async(Message.objects.filter)(dialog_in=dialog_objs)

    messages = await sync_to_async(
        lambda: [
                {"role": "system", "content": "say everything sarcastically but provide correct answers"},
            ] + [
                {"role": message.role, "content": message.content}
                for message in previous_messages
            ] + [
                {"role": "user", "content": user_input}
            ]
    )()

    response = await sync_to_async(openai.ChatCompletion.create)(
        model = "gpt-3.5-turno-0301",
        message=messages
    )

    answer = response.choices[0].message.content
    await save_assistant_message(dialog_str, answer)

    await message.reply(answer)

if __name__ == '__main__':
    executor.start_polling(dp)
