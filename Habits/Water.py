import asyncio
import random
import sqlite3
import time
import aioschedule
import os

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Database import prehabit_water_db, save_user_action
import Markups
import FSM_classes


async def habit_water(message: types.message, state: FSMContext):
    await prehabit_water_db(user_id=message.from_user.id, username=message.from_user.username)
    PreviewPhotoHabitWater = open('Habits/Water/' + random.choice(os.listdir('Habits/Water/')), 'rb')
    await bot.send_photo(message.from_user.id, PreviewPhotoHabitWater)
    await bot.send_message(message.from_user.id, 'Хотите настроить привычку или удалить её?', reply_markup=Markups.tune_habit)
    await FSM_classes.HabitWater.choose_action.set()


async def choose_habit_action(message: types.message, state: FSMContext):

    if message.text == 'Настроить привычку':
        await bot.send_message(message.from_user.id, 'Напишите сколько раз в день вы хотели бы пить воду.'
                                                     '\nНорма воды в день - 2 литра, выберите на сколько порций эту норму разделить (от 2 до 8)')
        db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
        cur_waterHabit = db_waterHabit.cursor()
        await FSM_classes.HabitWater.choose_amount_of_portion.set()

    if message.text == 'Удалить привычку':
        db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
        cur_waterHabit = db_waterHabit.cursor()
        habit = cur_waterHabit.execute('SELECT interval FROM water WHERE user_id = ? AND interval != 0',(message.from_user.id,)).fetchone()

        if habit is not None:
            cur_waterHabit.execute('UPDATE water SET interval = 0 WHERE user_id = ?', (message.from_user.id,))
            await bot.send_message(message.from_user.id, 'Ваша привычка успешно удалена!')
            db_waterHabit.commit()
            await save_user_action(user_id=message.from_user.id,action='waterHabitDeleted')

        else:
            await bot.send_message(message.from_user.id, 'У вас не настроена данная привычка!')


async def choose_habit_water_portions(message: types.message, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    if int(message.text) in range(2,9):
        cur_waterHabit.execute("UPDATE water SET amountOfPortions = ? WHERE user_id = ?", (int(message.text), message.from_user.id))

        await bot.send_message(message.from_user.id, 'Вы выбрали колличество приёмов воды: ' + message.text)
        await bot.send_message(message.from_user.id, 'Хотите работать над приемом воды по будням или выходным?',reply_markup=Markups.chooseScheduleWater)
        interval = int(round((1380-600)/int(message.text)))
        cur_waterHabit.execute("UPDATE water SET interval = ? WHERE user_id = ?",
                                      (interval, message.from_user.id))
        db_waterHabit.commit()
        await FSM_classes.HabitWater.choose_schedule.set()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка! Напишите колличество порций одной цифрой от 2 до 8!')
        await FSM_classes.HabitWater.choose_amount_of_portion.set()



async def choose_habit_water_schedule(message: types.message, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    if message.text == 'Будние':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('weekdays', message.from_user.id))
        db_waterHabit.commit()
    elif message.text == 'Выходные':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('weekends', message.from_user.id))
        db_waterHabit.commit()
    elif message.text == 'Вся неделя':
        cur_waterHabit.execute("UPDATE water SET schedule = ? WHERE user_id = ?",('both', message.from_user.id))
        db_waterHabit.commit()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка при вводе данных',reply_markup=Markups.chooseScheduleWater)
        await FSM_classes.HabitWater.choose_schedule.set()
    await bot.send_message(message.from_user.id,
                           'Вы успешно начали работу над приёмом воды!', reply_markup=Markups.backHabitRe)
    await save_user_action(user_id=message.from_user.id,action='waterHabitSet')

    await FSM_classes.MultiDialog.menu.set()

async def answer_water_schedule(callback_query: types.CallbackQuery, state: FSMContext):
    db_waterHabit = sqlite3.connect('Databases/Current_habits.db')
    cur_waterHabit = db_waterHabit.cursor()
    today = datetime.today()
    tableName = 'date_' + str(today)[0:10].replace('-','')
    db_mark = callback_query.data[-1]
    cur_waterHabit.execute(f'UPDATE waterDates SET {tableName} = ? WHERE user_id = ?', (db_mark,callback_query.from_user.id))
    db_waterHabit.commit()



