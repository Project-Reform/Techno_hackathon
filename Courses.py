from aiogram import Bot, types
from aiogram.dispatcher import FSMContext

import FSM_classes

from Token import Token
bot = Bot(Token)

import Markups
import FSM_classes
from AllCourses import Anxiety

async def precourse(message: types.Message, state: FSMContext):
    await FSM_classes.MultiDialog.courses.set()
    await bot.send_message(message.from_user.id, 'Выберите интересующий курс. В настоящий момент вам доступен курс: "Борьба с тревогой"',
                           parse_mode='html', reply_markup=Markups.courses_kb)

async def type_course(message: types.Message, state: FSMContext):
    if message.text == 'Борьба с тревогой':
        await FSM_classes.MultiDialog.course_anxiety.set()
        await Anxiety.pre_course_anxiety(message, state)

    if message.text in ['Подробнее о полной версии', 'Здоровый сон', 'Бодрое утро', 'Безмятежный вечер', 'Эмоциональное выгорание', 'Борьба с депрессией']:
        await bot.send_message(message.from_user.id, 'Полный доступ доступен в платной версии.'
                                                     '\nВ платной версии:'
                                                     '❇️25 медитаций'
                                                     '❇️10 дыхательных практик'
                                                     '❇️Таймер Помодоро'
                                                     '❇️Система ежедневных напоминаний и мотиваций'
                                                     '❇️Рекомендации по сну, питанию и отдыху от ведущих специалистов'
                                                     '\n\nХотите оформить подписку за 499 рублей в месяц?', parse_mode='html',
                               reply_markup=Markups.fullversion)

    if message.text == 'Оформить подписку':
        await bot.send_message(message.from_user.id, 'В настоящий момент вы можете написать @APecherkin по поводу подписки и сроков, когда она будет работать', parse_mode='html',
                               reply_markup=Markups.backCourseRe)