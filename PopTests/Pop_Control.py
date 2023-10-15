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

from Database import pre_points_test_control, points_test_control,save_user_action

import Markups
import FSM_classes

control_questions = ['1. Вы часто смотрите фильмы за компанию?'
                     '\n\nA) Да, почему бы не посмотреть хороший фильм по рекомендации друзей?'
                     '\nБ) Нет, я предпочитаю смотреть то, что интересно мне',
                     '2. Как вы считаете, реклама бывает честной?'
                     '\n\nA) Да, она вполне может раскрывать стоящие качества товара'
                     '\nБ) Нет, это реклама влияет на сознание и в любом случае несет в себе обман'
                     '\nВ) По-разному, в зависимости от того, что рекламируют',
                     '3. Вы выбирали свой жизненный путь сами или руководствовались мнением родителей?'
                     '\n\nA) Это был самостоятельный выбор'
                     '\nБ) Моим решением было положиться на родителей'
                     '\nВ) Мои взгляды на будущее совпали с родительскими'
                     '\nГ) Родители поддержали мой выбор'
                     '\nД) Родители не одобрили мой выбор, и я все сделал по-своему'
                     '\nЕ) Родители не одобрили мой выбор, и пришлось менять планы на жизнь'
                     '\nЖ) На мой выбор повлияли друзья и окружение',
                     '4. Представьте, что ваш близкий друг просит вас срочно одолжить весьма значительную сумму денег, а узнав, что вы не в силах его финансово поддержать, пообещал расстроиться. Ваши мысли на этот счет?'
                     '\n\nA) Он явно мной манипулирует, ему просто нужны деньги'
                     '\nБ) Он очень расстроен, должно быть, положение и правда безвыходное'
                     '\nВ) Он выглядит расстроенным, нужно подробнее узнать, в чем дело',
                     '5. Можете ли вы, не задумываясь, назвать три положительных качества вашего характера и вспомнить область, в которой добились определенных успехов?'
                     '\n\nA) Да'
                     '\nБ) Нет'
                     '\nВ) Не знаю',
                     '6. Доводилось ли вам совершать поступки, о которых вы впоследствии жалели?'
                     '\n\nA) Да'
                     '\nБ) Нет',
                     '7. Вы когда-нибудь бросали курить?'
                     '\n\nA) Нет, потому что не имею этой привычки'
                     '\nБ) Нет, потому что курю и все равно не смогу бросить'
                     '\nВ) Да, уже несколько раз пытаюсь бросить'
                     '\nГ) Да, и начинание увенчалось успехом',
                     '8. Вам приходилось завершать отношения по вашей инициативе?'
                     '\n\nA) Да, я предпочитаю расставить точки над И, если мои чувства угасли'
                     '\nБ) Нет, я не люблю делать больно другому и поэтому жду, когда мы окончательно остынем друг к другу'
                     '\nВ) Нет, инициатива, связанная с расставанием, исходила от партнера, а не от меня',
                     '9. Можете ли вы отказаться участвовать в споре или в разговоре, если они вам не интересны?'
                     '\n\nA) Да, мне не нужно никому доказывать свою правоту и вести бессмысленные беседы'
                     '\nБ) Нет, потому что последнее слово должно остаться за мно'
                     '\nВ) Нет, потому что мне неудобно обидеть собеседника, на мой взгляд, обрывать разговор невежливо',
                     '10. Вы строите планы на будущее?'
                     '\n\nA) Да, как правило, в письменном виде'
                     '\nБ) Стараюсь, но не всегда получается следовать намеченным планам'
                     '\nВ) Нет, я не люблю загадывать, что будет завтра']


# Keyboards
control_answer0 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_1'),
    InlineKeyboardButton('Б', callback_data='control_answer_0'))

control_answer1 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_2'),
    InlineKeyboardButton('Б', callback_data='control_answer_0'),
    InlineKeyboardButton('В', callback_data='control_answer_1'))

control_answer2 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_2'),
    InlineKeyboardButton('В', callback_data='control_answer_1'),
    InlineKeyboardButton('Г', callback_data='control_answer_1'),
    InlineKeyboardButton('Д', callback_data='control_answer_0'),
    InlineKeyboardButton('Е', callback_data='control_answer_2'),
    InlineKeyboardButton('Ж', callback_data='control_answer_1'))

control_answer3 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_2'),
    InlineKeyboardButton('В', callback_data='control_answer_1'))

control_answer4 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_1'),
    InlineKeyboardButton('В', callback_data='control_answer_2'))

control_answer5 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_2'),
    InlineKeyboardButton('Б', callback_data='control_answer_0'))

control_answer6 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_2'),
    InlineKeyboardButton('В', callback_data='control_answer_2'),
    InlineKeyboardButton('Г', callback_data='control_answer_0'))

control_answer7 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_1'),
    InlineKeyboardButton('В', callback_data='control_answer_2'))

control_answer8 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_1'),
    InlineKeyboardButton('В', callback_data='control_answer_0'))

control_answer9 = InlineKeyboardMarkup(resize_keyboard=True). add(
    InlineKeyboardButton('A', callback_data='control_answer_0'),
    InlineKeyboardButton('Б', callback_data='control_answer_1'),
    InlineKeyboardButton('В', callback_data='control_answer_2'))

control_answer_keyboards = [control_answer0, control_answer1, control_answer2, control_answer3, control_answer4, control_answer5, control_answer6, control_answer7, control_answer8, control_answer9]


async def pretest_control(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.test_control.set()
    await pre_points_test_control(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_control(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Нередко даже самая уверенная в себе личность идет на поводу обстоятельств или подчиняется чужим манипуляциям. '
                                                 '\nЧто и говорить, когда даже выбор одежды давно превратился в соревнование не только марок, но и умений эту вещь выгоднее продать.'
                                                 '\n\nТест подскажет вам, к какому типу людей относитесь вы, а в конце вас ждут рекомендации в зависимости от полученного вами результата. '
                                                 '\nПравила просты: читайте вопрос и выбирайте из предложенных вариантов один подходящий. Всего 10 вопросов', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await bot.send_message(message.from_user.id, text=control_questions[0], reply_markup=control_answer0)

async def answer_control(callback_query: types.CallbackQuery):
    point = callback_query.data[-1]
    db_control = sqlite3.connect('Databases/Result_Tests/POP_Control.db')
    cur_control = db_control.cursor()
    one = int(1)
    two = int(2)
    cur_control.execute("UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if point == '2':
        cur_control.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif point == '1':
        cur_control.execute("UPDATE points SET points = points + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    db_control.commit()
    if int(cur_control.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 10:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=control_questions[int(cur_control.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])],
                                    message_id=callback_query.message.message_id, reply_markup=control_answer_keyboards[int(cur_control.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])])
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if int(cur_control.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 10:
            await bot.send_message(callback_query.from_user.id, 'Вы отличаетесь редкой независимостью от чужого мнения! '
                                                                '\n\nВы строите свою жизнь, опираясь на собственные принципы, а не на интересы окружающих, а также способны распознать манипуляцию и пресечь попытку управлять вами. '
                                                                '\nНо будьте осторожны, категоричность суждений может вызывать у ваших близких сложности при общении с вами, рассмотрев в вас излишне жесткого или недоверчивого человека. '
                                                                '\nПомните, что открытя улыбка располагает людей к вам и при этом вовсе не обязывает идти у кого-то на поводу', reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Control')
        elif (int(cur_control.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 9 ) and (int(cur_control.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) < 16):
            await bot.send_message(callback_query.from_user.id,
                                   'Выстраивая взаимоотношения с людьми и собственную жизнь, вы достаточно хорошо разбираетесь в причинно-следственных связях. '
                                   '\nПовлиять на вашу личность не так-то просто!'
                                   '\nНо иногда вы все же можете попасть впросак. Чтобы лучше ориентироваться в происходящем, вы можете узнать психологические приемы, которые помогают управлять людьми, и чаще действовать в своих интересах.',
                                   reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Control')
        else:
            await bot.send_message(callback_query.from_user.id,
                                   'Возможно, не все решения в жизни вы приняли, руководствуясь собственными интересами. '
                                   '\nНо не бойтесь иногда настаивать на своем и действовать немного эгоистичнее. '
                                   '\nВы сможете найти золотую середину, не отпугнув окружающих, но при этом начав жить по своим правилам! '
                                   '\nХорошим решением будет повышение самооценки. Помня о своей ценности для мира, избавившись от комплексов и полюбив себя, вы можете изменить жизнь и взять ее в свои руки.',
                                   reply_markup=Markups.backIn)
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Control')


def register_handlers_Pop_Control(dp : Dispatcher):
    dp.register_callback_query_handler(answer_control, text=['control_answer_0', 'control_answer_1', 'control_answer_2'])