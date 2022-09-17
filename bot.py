from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ContentType
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from datetime import datetime
import random


from time import sleep #import sleep for timeout set
logfilename = 'log.csv' #difining logfile
storage=MemoryStorage() #defining storage in memory
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)
button1 = KeyboardButton('Овен')
button2 = KeyboardButton('Телец')
button3 = KeyboardButton('Близнецы')
button4 = KeyboardButton('Рак')
button5 = KeyboardButton('Лев')
button6 = KeyboardButton('Дева')
button7 = KeyboardButton('Весы')
button8 = KeyboardButton('Скорпион')
button9 = KeyboardButton('Стрелец')
button10 = KeyboardButton('Козерог')
button11 = KeyboardButton('Водолей')
button12 = KeyboardButton('Рыбы')
#keyboard buttons for every zodiac sign

keyboard1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button1).add(button2).add(button3).add(button4).add(button5).add(button6).add(button7).add(button8).add(button9).add(button10).add(button11).add(button12)
#whole keyboard


class FSMSay(StatesGroup):
    first = State()
    second = State()
#defining bot states

@dp.message_handler()
async def command_start(message : types.Message):
    await bot.send_message(message.from_user.id, 'Привет! Узнай вашу совместимость😀 Данные берутся со звезд онлайн, зависят от момента времени, разработчик ответственности не несет! Выбери свой знак:', reply_markup=keyboard1)
    await FSMSay.first.set() #setting first state
    userid = message.chat.id
    user_first_name = str(message.chat.first_name)
    user_last_name = str(message.chat.last_name)
    user_username = str(message.chat.username)
    timenow = datetime.now()
    with open(logfilename, 'a', encoding="utf-8") as file_object:
        file_object.write(f'"{timenow}","{userid}","{user_username}","{user_first_name} {user_last_name}","request","{message.text}"\n')
#logging


@dp.message_handler(state=FSMSay.first)
async def command_start(message : types.Message, state: FSMContext):
    await FSMSay.second.set() #setting second state
    async with state.proxy() as data:
        data['znak1'] = message.text #saving first sign in state proxy storage
    await bot.send_message(message.from_user.id, 'Выбери его/ее знаек:', reply_markup=keyboard1)
    userid = message.chat.id
    user_first_name = str(message.chat.first_name)
    user_last_name = str(message.chat.last_name)
    user_username = str(message.chat.username)
    timenow = datetime.now()
    with open(logfilename, 'a', encoding="utf-8") as file_object:
        file_object.write(f'"{timenow}","{userid}","{user_username}","{user_first_name} {user_last_name}","request","{message.text}"\n')
#logging

@dp.message_handler(state=FSMSay.second)
async def command_start(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['znak2'] = message.text
    if data['znak1'] == 'Рак' or data['znak2'] == 'Рак':
        result = 'Совместимость ' + data['znak1'] + ' и ' + data['znak2']+ ' = ' + random.choice(['🔥','❤','🤰'])
    else:
        result = 'Совместимость ' + data['znak1'] + ' и ' + data['znak2']+ ' = ' + random.choice(['🔥','❤','💩','🤰','😔','💩'])
    #my space algorithm =D
    await bot.send_message(message.from_user.id, result)
    await state.finish() #closing second state
    sleep(2)
    await bot.send_message(message.from_user.id, 'Понравилось? Давай еще =)')
    sleep(1)
    await bot.send_message(message.from_user.id, 'Выбери свой знак:', reply_markup=keyboard1)
    await FSMSay.first.set()
    userid = message.chat.id
    user_first_name = str(message.chat.first_name)
    user_last_name = str(message.chat.last_name)
    user_username = str(message.chat.username)
    timenow = datetime.now()
    with open(logfilename, 'a', encoding="utf-8") as file_object:
        file_object.write(f'"{timenow}","{userid}","{user_username}","{user_first_name} {user_last_name}","request","{message.text}","{result}"\n')
    



executor.start_polling(dp, skip_updates=True)
