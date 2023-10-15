import asyncio
import os
import random
import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
from Database import db_start, data_profile, save_user_action

import Markups
import FSM_classes


async def type_practices(message: types.Message):
    await FSM_classes.MultiDialog.practices.set()
    await bot.send_message(message.from_user.id, 'Выберите тип практики',
                           parse_mode='html', reply_markup=Markups.Practice_kb)
async def allreply_practices(message: types.Message):
    if message.text == 'Дыхательные практики':
        DuhPractice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Dexr1 = types.KeyboardButton('Расслабление через напряжение (6 мин)')
        Dexr2 = types.KeyboardButton('Дыхание квадрат (4 мин)')
        Dexr3 = types.KeyboardButton('Асимметричное дыхание (2 мин)')
        DuhPractice.add(Dexr1, Dexr2, Dexr3)
        await bot.send_message(message.chat.id,
                               'Выберите дыхательную практику', reply_markup=DuhPractice)

    if message.text == 'Медитативные практики':
        MedPractice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Mexr1 = types.KeyboardButton('Яблоневый сад (4 мин)')
        Mexr2 = types.KeyboardButton('Полёт к звезде (7 мин)')
        Mexr3 = types.KeyboardButton('Путешествие на воздушном шаре (5 мин)')
        MedPractice.add(Mexr1, Mexr2, Mexr3)
        await bot.send_message(message.chat.id,
                               'Выберите медитативную практику', reply_markup=MedPractice)

    if message.text == "Расслабление через напряжение (6 мин)":
        await save_user_action(user_id=message.from_user.id, action='Расслабление через напряжение (6 мин)')

        await bot.send_message(message.chat.id,
                               "Практика направлена на то, чтобы через физическое напряжение и расслабление добиться расслабления нашего ума. "
                               "Рекомендуется пойти в отдалённое, тихое место и занять удобную позу.")
        ExVisualPhoto1 = open('Exercises/Расслабление через напряжение.jpg', 'rb')
        ExVisualAudio1 = open('Exercises/Расслабление через напряжение.mp3',
                              'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto1)
        await bot.send_audio(message.chat.id, ExVisualAudio1, reply_markup=Markups.endpractice)

    elif message.text == "Дыхание квадрат (4 мин)":
        await save_user_action(user_id=message.from_user.id, action="Дыхание квадрат (4 мин)")
        await bot.send_message(message.chat.id,
                               "Вдох, выдох и пауза примерно равны друг другу по длительности, комфортный ритм – примерно 4 секунд")
        ExVisualAudio2 = open('Exercises/Дыхание квадрат.mp3', 'rb')
        ExVisualPhoto2 = open('Exercises/Квадрат дыхания.jpg', 'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto2)
        await bot.send_audio(message.chat.id, ExVisualAudio2, reply_markup=Markups.endpractice)
    elif message.text == "Асимметричное дыхание (2 мин)":
        await save_user_action(user_id=message.from_user.id, action="Асимметричное дыхание (2 мин)")

        await bot.send_message(message.chat.id,
                               "Вдыхать нужно через нос, а выдыхать через рот  делать выдох в 5 раз длиннее вдоха (рекомендуется 2 секунд вдох, 10 секунд выдох")
        ExVisualAudio3 = open('Exercises/Асимметричное дыхание.mp3', 'rb')
        ExVisualPhoto3 = open('Exercises/Асимметричное дыхание.png', 'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto3)
        await bot.send_audio(message.chat.id, ExVisualAudio3, reply_markup=Markups.endpractice)

    if message.text == "Яблоневый сад (4 мин)":
        await save_user_action(user_id=message.from_user.id, action="Яблоневый сад (4 мин)")
        await bot.send_message(message.chat.id,
                               "Рекомендуется занять удобную позу сидя и расслабиться, если есть возможность лечь на коврик на спину в позу морской звезды")
        ExVisualAudio1 = open('Exercises/Яблоневый сад.mp3', 'rb')
        ExVisualPhoto1 = open('Exercises/Яблоневый сад.jpg', 'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto1)
        await bot.send_audio(message.chat.id, ExVisualAudio1, reply_markup=Markups.endpractice)
    elif message.text == "Путешествие к звезде (7 мин)":
        await save_user_action(user_id=message.from_user.id, action="Полёт к звезде (7 мин)")
        await bot.send_message(message.chat.id,
                               "Рекомендуется занять удобную позу сидя и расслабиться, если есть возможность лечь на коврик на спину в позу морской звезды")
        ExVisualAudio2 = open('Exercises/Путешествие к звезде.mp3', 'rb')
        ExVisualPhoto2 = open('Exercises/Путешествие к звезде.jpg', 'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto2)
        await bot.send_audio(message.chat.id, ExVisualAudio2, reply_markup=Markups.endpractice)
    elif message.text == "Полёт на воздушном шаре (5 мин)":
        await save_user_action(user_id=message.from_user.id, action="Путешествие на воздушном шаре (5 мин)")
        await bot.send_message(message.chat.id,
                               "Рекомендуется занять удобную позу сидя и расслабиться, если есть возможность лечь на коврик на спину в позу морской звезды")
        ExVisualAudio3 = open('Exercises/Полет на воздушном шаре.mp3', 'rb')
        ExVisualPhoto3 = open('Exercises/Полёт на воздушном шаре.jpg', 'rb')
        await bot.send_photo(message.chat.id, ExVisualPhoto3)
        await bot.send_audio(message.chat.id, ExVisualAudio3, reply_markup=Markups.endpractice)

    if message.text == 'Выбрать другую практику':
        await type_practices(message)





