import asyncio
import sqlite3

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, timedelta

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())

from Database import pre_points_test_control, points_test_control, pre_points_test_selfefficacy, \
    points_test_selfefficacy

import Markups
import FSM_classes

selfefficacy_questions = ['1) Если я как следует постараюсь, то всегда найду решение даже сложной проблемы',
                     '2) Если мне что-нибудь мешает, то я все же нахожу пути достижения своей цели',
                     '3) Мне довольно просто удается достичь своих целей',
                     '4) В неожиданных ситуациях я всегда знаю, как я должен себя вести',
                     '5) При непредвиденно возникающих трудностях я верю, что смогу с ними справиться',
                     '6) Если я приложу достаточно усилий, то смогу справиться с большинством проблем',
                     '7) Я готов к любым трудностям, поскольку полагаюсь на собственные способности',
                     '8) Если передо мной встает какая-либо проблема, то я обычно нахожу несколько вариантов ее решения',
                     '9) Я могу что-нибудь придумать даже в безвыходных на первый взгляд ситуациях',
                     '10) Я обычно способен держать ситуацию под контролем']

selfefficacy_answer = InlineKeyboardMarkup(resize_keyboard=True, row_width=1). add(
    InlineKeyboardButton('Абсолютно неверно (-)', callback_data='selfefficacy_answer_1'),
    InlineKeyboardButton('Едва ли верно (-+)', callback_data='selfefficacy_answer_2'),
    InlineKeyboardButton('Скорее верно (+-)', callback_data='selfefficacy_answer_3'),
    InlineKeyboardButton('Совершенно верно (+)', callback_data='selfefficacy_answer_4'))

async def pretest_selfefficacy(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.test_selfefficacy.set()
    await pre_points_test_selfefficacy(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_selfefficacy(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Самоэффективность - уверенность в успехе собственного поведения.'
                                                 '\nВ понятие вкладывается возможность оценивать умение людей осознавать свои способности и использовать их наилучшим образом. '
                                                 'При этом особое внимание придается тому, что при более чем скромных способностях умелое их использование позволяет человеку достичь высоких результатов.'
                                                 '\nВ то же время наличие высокого потенциала автоматически не гарантирует высокие результаты, '
                                                 'если человек не верит в возможность применить этот потенциал на практике и не пытается воспользоваться всем тем, что дано ему природой и обществом.'
                                                 '\n\nТест, который позволяет относительно измерить ваш уровень самоэффективности в настоящее время состоит из 10 утверждений'
                                                 ' на которые вам нужно дать ответ в четырехбальной системе и оценить так ли это.'
                                                 '\n\nПриступим к тесту!', reply_markup=types.ReplyKeyboardRemove())
    timeNow = datetime.now()
    timeNow = str(timeNow)[:-7]
    db_user_interactions = sqlite3.connect('Databases/user_interactions.db')
    cur_user_interactions = db_user_interactions.cursor()
    cur_user_interactions.execute("INSERT INTO users VALUES(?, ?, ?)",
                                  (message.from_user.id, 'Psy_selfefficacy', timeNow))
    db_user_interactions.commit()
    await asyncio.sleep(5)
    await bot.send_message(message.from_user.id, text=selfefficacy_questions[0], reply_markup=selfefficacy_answer)

async def answer_selfefficacy(callback_query: types.CallbackQuery):
    db_selfefficacy = sqlite3.connect('Databases/Result_Tests/PSY_Selfefficacy.db')
    cur_selfefficacy= db_selfefficacy.cursor()
    one = int(1)
    two = int(2)
    three = int(3)
    four = int(4)
    cur_selfefficacy.execute("UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if callback_query.data[-1] == '1':
        cur_selfefficacy.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    elif callback_query.data[-1] == '2':
        cur_selfefficacy.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif callback_query.data[-1] == '3':
        cur_selfefficacy.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (three, callback_query.from_user.id))
    elif callback_query.data[-1] == '4':
        cur_selfefficacy.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (four, callback_query.from_user.id))
    db_selfefficacy.commit()
    if int(cur_selfefficacy.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 10:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=selfefficacy_questions[int(cur_selfefficacy.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])],
                                    message_id=callback_query.message.message_id, reply_markup=selfefficacy_answer[int(cur_selfefficacy.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])])
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if int(cur_selfefficacy.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 27:
            await bot.send_message(callback_query.from_user.id,
                                   'Ваша самоэффективность на низком уровне, советуем вам задуматься о вере в себя!'
                                   '\nСамоэффективность — вера человека в его способность производить необходимый уровень результата, влияющего на события, которые влияют на его жизнь.'
                                   '\n\nЛюди с низкой самоэффективностью имеют низкие устремления и слабую приверженность целям, которые они себе ставят.'
                                   '\n\nУспех повышает самоэффективность, поражение — понижает, особенно если поражение случилось до того, как ты стал уверенным в себе'
                                   'Лучший источник самоэффективности — это ощущение своего мастерства.'
                                   'Неудачи в человеческих устремлениях служат полезной цели — научить человека, что успех требует последовательных действий'
                                   '\nВ самые сложные и важные моменты мы чувствуем волнение, страх, тревогу.'
                                   'Когда твое сердце уходит в пятки, это значит, что ты делаешь что-то важное и выходишь из зоны своей трусости.'
                                   'Когда ты делаешь что-то для тебя важное, испытывать волнение — нормально. Наслаждайся волнением и все равно действуй!',
                                   reply_markup=Markups.backIn)
        elif (int(cur_selfefficacy.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 26 ) and (int(cur_selfefficacy.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 36):
            await bot.send_message(callback_query.from_user.id,
                                   'Ваша самоэффективность на среднем уровне, верьте больше в себя!'
                                   '\nСамоэффективность — вера человека в его способность производить необходимый уровень результата, влияющего на события, которые влияют на его жизнь.'
                                   '\n\nЛюди с низкой самоэффективностью имеют низкие устремления и слабую приверженность целям, которые они себе ставят.'
                                   '\n\nУспех повышает самоэффективность, поражение — понижает, особенно если поражение случилось до того, как ты стал уверенным в себе'
                                   'Лучший источник самоэффективности — это ощущение своего мастерства.'
                                   'Неудачи в человеческих устремлениях служат полезной цели — научить человека, что успех требует последовательных действий'
                                   '\nВ самые сложные и важные моменты мы чувствуем волнение, страх, тревогу.'
                                   'Когда твое сердце уходит в пятки, это значит, что ты делаешь что-то важное и выходишь из зоны своей трусости.'
                                   'Когда ты делаешь что-то для тебя важное, испытывать волнение — нормально. Наслаждайся волнением и все равно действуй!',
                                   reply_markup=Markups.backIn)
        else:
            await bot.send_message(callback_query.from_user.id,
                                   'Поздравляем! У вас высокий уровень самоэффективности! Продолжайте в том же духе и вы добьетесь всего, чего пожелаете!'
                                   '\nВ области мышления высокая самоэффективность облегчает процесс принятия решений и проявляется в разнообразных общих способностях, включая академические достижения и повышенную мотивацию к осуществлению активных действий, особенно в трудных ситуациях. '
                                   'Люди с высокой самоэффективностью предпочитают браться за более сложные задачи, они ставят перед собой более высокие цели и упорнее их добиваются!',
                                   reply_markup=Markups.backIn)


def register_handlers_Psy_selfefficacy(dp : Dispatcher):
    dp.register_callback_query_handler(answer_selfefficacy, text=['selfefficacy_answer_1', 'selfefficacy_answer_2', 'selfefficacy_answer_3', 'selfefficacy_answer_4'])