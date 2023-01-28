# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import database
import functions as fn

API_TOKEN = 'PAST_YOUR_TOKEN_HERE'

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = database.SQLiter("db.db")


async def on_startup(_):
    print('Бот вышел онлайн.')


ikb = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton('English 🇺🇸', callback_data='English')
b2 = InlineKeyboardButton('Русский 🇷🇺', callback_data='Russian')
b3 = InlineKeyboardButton('*', callback_data='*')
b4 = InlineKeyboardButton('.', callback_data='.')
b5 = InlineKeyboardButton('+', callback_data='+')
b6 = InlineKeyboardButton('•', callback_data='•')
b7 = InlineKeyboardButton('🟢', callback_data='🟢')
b8 = InlineKeyboardButton('🔴', callback_data='🔴')
b9 = InlineKeyboardButton('🔶', callback_data='🔶')
b10 = InlineKeyboardButton('0️⃣', callback_data='0️⃣')
b11 = InlineKeyboardButton('-', callback_data='-')
b12 = InlineKeyboardButton('–', callback_data='–')
b13 = InlineKeyboardButton('—', callback_data='—')
b14 = InlineKeyboardButton('=', callback_data='=')
b15 = InlineKeyboardButton('🟩', callback_data='🟩')
b16 = InlineKeyboardButton('🟥', callback_data='🟥')
b17 = InlineKeyboardButton('🔷', callback_data='🔷')
b18 = InlineKeyboardButton('1️⃣', callback_data='1️⃣')
bm = InlineKeyboardButton('Morse', callback_data='Morse')
bt = InlineKeyboardButton('Text', callback_data='Text')
ikb.row(b1, b2).row(b3, b4, b5, b6).row(b7, b8, b9, b10).row(b11, b12, b13, b14).row(b15, b16, b17, b18).row(bm, bt)


@dp.message_handler(commands=['start'])
async def starting(message: types.Message):
    if not db.exists_user(message.from_user.id):  # если юзера нет в базе данных
        db.add_to_db(message.from_user.id)  # добавить пользователя в базу с настройками по умолчанию
        await bot.send_message(message.from_user.id, await fn.start_msg(message.from_user.id))
    else:
        await bot.send_message(message.from_user.id, await fn.start_msg(message.from_user.id))


@dp.message_handler(commands=['settings'])
async def change_settings(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'The first row of buttons is for language selection.\n'
                           'The second and third rows are to select a dot.\n'
                           'The fourth and fifth rows are to select a dash.\n'
                           'The sixth row is for selecting the mode.',  # объяснить какие кнопки что настраивают
                           reply_markup=ikb)


@dp.message_handler(commands=['reset'])
async def reset_settings(message: types.Message):
    db.reset_all_default(message.from_user.id)  # сбросить все настройки по умолчанию
    await bot.send_message(message.from_user.id, 'The settings have been reset')


@dp.callback_query_handler(text=['English', 'Russian', '*', '.', '+', '•', '🟢', '🔴', '🔶', '0️⃣',
                                 '-', '–', '—', '=', '🟩', '🟥', '🔷', '1️⃣', 'Morse', 'Text'])
async def get_language(call: types.CallbackQuery):
    data = call.data
    if data in ['English', 'Russian']:
        db.update_language(call.from_user.id, data)
        await call.answer()
        if call.message.text != await fn.edit_settings_msg(call.from_user.id):
            await call.message.edit_text(await fn.edit_settings_msg(call.from_user.id), reply_markup=ikb)
    elif data in ['*', '.', '+', '•', '🟢', '🔴', '🔶', '0️⃣']:
        db.update_dot(call.from_user.id, data)
        await call.answer()
        if call.message.text != await fn.edit_settings_msg(call.from_user.id):
            await call.message.edit_text(await fn.edit_settings_msg(call.from_user.id), reply_markup=ikb)
    elif data in ['-', '–', '—', '=', '🟩', '🟥', '🔷', '1️⃣']:
        db.update_dash(call.from_user.id, call.data)
        await call.answer()
        if call.message.text != await fn.edit_settings_msg(call.from_user.id):
            await call.message.edit_text(await fn.edit_settings_msg(call.from_user.id), reply_markup=ikb)
    elif data in ['Morse', 'Text']:
        db.update_mode(call.from_user.id, data)
        await call.answer()
        if call.message.text != await fn.edit_settings_msg(call.from_user.id):
            await call.message.edit_text(await fn.edit_settings_msg(call.from_user.id), reply_markup=ikb)


@dp.message_handler()
async def translate(message: types.Message):
    await bot.send_message(message.from_user.id,
                           await fn.translator(message.from_user.id, message.text),
                           parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
