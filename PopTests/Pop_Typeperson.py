import asyncio
import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Database import pre_points_test_typeperson, points_test_typeperson, save_user_action

import Markups
import FSM_classes

typeperson_questions = [' 1. Мне снятся яркие, причудливые сны.',
                          '2. Приступая к какой-нибудь работе, я не люблю связывать себя планом действий, а во многом следую интуиции.',
                          '3. На некоторые важные мои решения оказывают влияние окружающие.',
                          '4. Увлекаюсь театром, поэзией, живописью.',
                          '5. Я человек непрактичный.',
                          '6. Легко могу представить себя каким-нибудь животным.',
                          '7. Угнетает, когда в квартире всё строго расставлено и у каждой вещи есть своё определённое место.',
                          '8. Меня легко обидеть или задеть.',
                          '9. Когда что-нибудь случается с близким мне человеком, я чувствую себя так, словно это произошло со мной.',
                          '10. В кино, театре или художественной литературе я предпочитаю интригующую недосказанность полной ясности сюжетной линии.',
                          '11. Мои чувства незаметно перетекают одно в другое.',
                          '12. Бывает, я слышу, что меня кто-то зовёт по имени, но, оглянувшись, никого не нахожу.',
                          '13. Немного скучной организацией можно назвать ту, в которой все чётко представляют себе свои обязанности и абсолютно ясно, кто за что отвечает.',
                          '14. Люблю предаваться мечтам и фантазиям.',
                          '15. Моя открытость и излишняя близость с некоторыми людьми доставляют мне проблемы.',
                          '16. Мне легко вспомнить свои детские ощущения и чувства.',
                          '17. Непросто провести чёткие границы между людьми с психологическими проблемами и теми, кто их практически не имеет.',
                          '18. Замечательные родители — сами в душе немного дети.']

typeperson_answer = InlineKeyboardMarkup(resize_keyboard=True, row_width=1). add(
    InlineKeyboardButton('Совершенно верно', callback_data='typeperson_answer_5'),
    InlineKeyboardButton('Скорее да, чем нет', callback_data='typeperson_answer_4'),
    InlineKeyboardButton('Иногда', callback_data='typeperson_answer_3'),
    InlineKeyboardButton('Скорее нет, чем да', callback_data='typeperson_answer_2'),
    InlineKeyboardButton('Абсолютно нет', callback_data='typeperson_answer_1'))

async def pretest_typeperson(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.test_selfefficacy.set()
    await pre_points_test_typeperson(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_typeperson(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Тест поможет узнать вам сильные стороны и скрытые ресурсы личности.'
                                                 'Но помните, тест служит своеобразным индикатором, который только примерно может определить присущие Вам качества.'
                                                 '\n\nВам будет предложено 18 утверждений, оцените их по 5-балльной шкале, в какой степени они про вас'
                                                 '\nПриступим к тесту!', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(3)
    await bot.send_message(message.from_user.id, text=typeperson_questions[0], reply_markup=typeperson_answer)

async def answer_typeperson(callback_query: types.CallbackQuery):
    db_typeperson = sqlite3.connect('Databases/Result_Tests/POP_Typeperson.db')
    cur_typeperson= db_typeperson.cursor()
    one, two, three, four, five = 1,2,3,4,5
    cur_typeperson.execute("UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if callback_query.data[-1] == '1':
        cur_typeperson.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    elif callback_query.data[-1] == '2':
        cur_typeperson.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif callback_query.data[-1] == '3':
        cur_typeperson.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (three, callback_query.from_user.id))
    elif callback_query.data[-1] == '4':
        cur_typeperson.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (four, callback_query.from_user.id))
    elif callback_query.data[-1] == '5':
        cur_typeperson.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (five, callback_query.from_user.id))
    db_typeperson.commit()
    if int(cur_typeperson.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 18:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=typeperson_questions[int(cur_typeperson.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])],
                                    message_id=callback_query.message.message_id, reply_markup=typeperson_answer)
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if int(cur_typeperson.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 26:
            await bot.send_message(callback_query.from_user.id,
                                   'Вы получаете не слишком много наслаждения от плотских радостей жизни. Можете испытывать некоторые затруднения в контактах с окружающими. '
                                   '\nЗато вы довольно-таки основательны, вас сложно вывести из равновесия. Вы редко принимаете скоропалительные решения, руководствуетесь не эмоциями, а логикой. '
                                   '\nСовет: не замыкайтесь в себе и проявляйте больше нежности к домочадцам.',
                                   reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Typeperson')
        elif (int(cur_typeperson.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 25 ) and (int(cur_typeperson.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 50):
            await bot.send_message(callback_query.from_user.id,
                                   'Ваш склад психики близок к золотой середине, что очень даже неплохо. '
                                   '\nПомните, умеренность может стать для вас залогом успеха!',
                                   reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Typeperson')
        else:
            await bot.send_message(callback_query.from_user.id,
                                   'Вероятно, вы достаточно чувствительны к внешним раздражителям. Сильнее остальных страдаете от громких звуков и яркого света. '
                                   'Не лишены мнительности и, скорее всего, подвержены смене настроения. '
                                   '\nЛюди с такой психической организацией бывают творческими личностями. '
                                   '\nСтарайтесь по возможности спокойнее реагировать на всё происходящее и не открывайте душу первому встречному.',
                                   reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Typeperson')


def register_handlers_Pop_typeperson(dp : Dispatcher):
    dp.register_callback_query_handler(answer_typeperson, text=['typeperson_answer_1', 'typeperson_answer_2', 'typeperson_answer_3', 'typeperson_answer_4', 'typeperson_answer_5'])