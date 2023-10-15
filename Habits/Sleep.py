import asyncio
import sqlite3
import time
import aioschedule
import os
import random

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Database import prehabit_sleep_db, save_user_action
import Markups
import FSM_classes


async def habit_sleep(message: types.message, state: FSMContext):
    await prehabit_sleep_db(user_id=message.from_user.id, username=message.from_user.username)
    PreviewPhotoHabitSleep = open('Habits/Sleep/' + random.choice(os.listdir('Habits/Sleep/')), 'rb')
    await bot.send_photo(message.from_user.id, PreviewPhotoHabitSleep)
    await bot.send_message(message.from_user.id, 'Хотите настроить привычку или удалить её?', reply_markup=Markups.tune_habit)
    await FSM_classes.HabitSleep.choose_action.set()

async def choose_habit_action(message: types.message, state: FSMContext):

    if message.text == 'Настроить привычку':
        await bot.send_message(message.from_user.id, 'Напишите время желаемого утреннего пробуждения по Московскому времени (GMT+3) в формате ЧЧ:ММ (например: 07:05)')
        await FSM_classes.HabitSleep.choose_wakeup.set()

    if message.text == 'Удалить привычку':
        db_sleephabit = sqlite3.connect('Databases/Current_habits.db')
        cur_sleephabit = db_sleephabit.cursor()
        habit_active = cur_sleephabit.execute('SELECT active FROM sleep WHERE user_id = ? AND active != 0',
                                       (message.from_user.id,)).fetchone()
        if habit_active is not None:
            cur_sleephabit.execute('UPDATE sleep SET active = 0 WHERE user_id = ?', (message.from_user.id,))
            await bot.send_message(message.from_user.id, 'Ваша привычка успешно удалена!')
            db_sleephabit.commit()
            await save_user_action(user_id=message.from_user.id, action='Привычка "Сон" УДАЛЕНА')
        else:
            await bot.send_message(message.from_user.id, 'У вас не настроена данная привычка!')

async def choose_habit_sleep_wakeup(message: types.message, state: FSMContext):
    db_sleephabit = sqlite3.connect('Databases/Current_habits.db')
    cur_sleephabit = db_sleephabit.cursor()
    timewakeup = message.text.split(':')
    # cur_sleephabit.execute("UPDATE sleep SET active = timewakeup WHERE user_id = ?",
    #                        (message.text, message.from_user.id))
    if len(timewakeup) == 2:
        if timewakeup[0].isdigit() and timewakeup[1].isdigit():
            if int(timewakeup[0]) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24] and int(timewakeup[1]) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]:
                cur_sleephabit.execute("UPDATE sleep SET wakeup = ? WHERE user_id = ?", (message.text, message.from_user.id))
                db_sleephabit.commit()
                await bot.send_message(message.from_user.id, 'Вы выбрали время пробуждения: '+message.text)
                await bot.send_message(message.from_user.id, 'Теперь напишите время отхода ко сну по Московсокму времени (GMT+3) в формате ЧЧ:ММ (например: 22:45).'
                                                             '\nМы рекомендуем оставлять на сон не менее 7-8 часов!')
                await FSM_classes.HabitSleep.choose_bedtime.set()
            else:
                await bot.send_message(message.from_user.id,
                                       'Ошибка! Напишите время желаемого утреннего пробуждения в формате ЧЧ:ММ (например: 07:05)')
                await FSM_classes.HabitSleep.choose_wakeup.set()
        else:
            await bot.send_message(message.from_user.id,
                                   'Ошибка! Напишите время желаемого утреннего пробуждения в формате ЧЧ:ММ (например: 07:05)')
            await FSM_classes.HabitSleep.choose_wakeup.set()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка! Напишите время желаемого утреннего пробуждения в формате ЧЧ:ММ (например: 07:05)')
        await FSM_classes.HabitSleep.choose_wakeup.set()




async def choose_habit_sleep_bedtime(message: types.message, state: FSMContext):
    db_sleephabit = sqlite3.connect('Databases/Current_habits.db')
    cur_sleephabit = db_sleephabit.cursor()
    timebed = message.text.split(':')
    if len(timebed) == 2:
        if timebed[0].isdigit() and timebed[1].isdigit():
            if int(timebed[0]) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24] and int(timebed[1]) in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]:
                cur_sleephabit.execute("UPDATE sleep SET bedtime = ? WHERE user_id = ?", (message.text, message.from_user.id))
                db_sleephabit.commit()
                await FSM_classes.MultiDialog.menu.set()
                await bot.send_message(message.from_user.id, 'Вы выбрали время отхода ко сну: ' + message.text + '\nПоздравляем! Вы начали работу со своим сном!', reply_markup=Markups.backHabitRe)
                cur_sleephabit.execute("UPDATE sleep SET active = 1 WHERE user_id = ?",
                                       (message.from_user.id,))
                db_sleephabit.commit()
            else:
                await bot.send_message(message.from_user.id,
                                       'Ошибка! Напишите время отхода ко сну в формате ЧЧ:ММ (например: 22:45)')
                await FSM_classes.HabitSleep.choose_bedtime.set()
        else:
            await bot.send_message(message.from_user.id,
                                   'Ошибка! Напишите время отхода ко сну в формате ЧЧ:ММ (например: 22:45)')
            await FSM_classes.HabitSleep.choose_bedtime.set()
    else:
        await bot.send_message(message.from_user.id,
                               'Ошибка! Напишите время отхода ко сну в формате ЧЧ:ММ (например: 22:45)')
        await FSM_classes.HabitSleep.choose_bedtime.set()


# async def scheduler():
#             aioschedule.every().day.at("17:45").do(choose_your_dinner)
#         while True:
#             await aioschedule.run_pending()
#             await asyncio.sleep(1)
#

