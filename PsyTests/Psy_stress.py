from Database import db_start, data_profile, pre_points_test_stress, points_test_stress, pre_answers_test_stress, save_user_action
import asyncio
import sqlite3
import Markups
import FSM_classes
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


answers = InlineKeyboardMarkup().add(InlineKeyboardButton('Часто/сильно', callback_data='answer_y'),
                                     InlineKeyboardButton(
    'Редко/иногда', callback_data='answer_m'),
    InlineKeyboardButton('Нет/Никогда', callback_data='answer_n'))

questionstr = ["1. У меня слишком высокое кровяное давление",
               "2. У меня бывают приступы тошноты",
               "3. Я боюсь заболеть",
               "4. Я чувствую себя беспомощным",
               "5. У меня бывают кошмары",
               "6. У меня дрожат ноги/руки",
               "7. Я часто просыпаюсь",
               "8. Мои кисти/стопы холодные",
               "9. Я не могу правильно дышать",
               "10. Я чувствую слабость",
               "11. У меня потные руки/лоб",
               "12. У меня боли в шее",
               "13. Я не могу сосредоточиться",
               "14. У меня нарушено пищеварение",
               "15. Я страдаю низким кровяным давлением",
               "16. Я раздражителен в личной жизни",
               "17. Я раздражителен на работе",
               "18. У меня бывают приступы мигрени",
               "19. Я испытываю внутренне беспокойство",
               "20. Я страдаю от болей в желудке",
               "21. Мне постоянно хочется спать",
               "22. Мое сердце бешено стучит или прерывисто бьется",
               "23. У меня словно ком застревает в горле",
               "24. Я чувствую стеснение в груди",
               "25. Я нервозен	",
               "26. Меня бросает в жар	",
               "27. Слезы душат меня	",
               "28. У меня бывают головные боли	",
               "29. Бывают спазмы определенных групп мышц	",
               "30. Меня одолевают страхи	",
               "31. У меня бывают головокружения	",
               "32. У меня болит спина и поясница	",
               "33. Я не могу уснуть"]


async def pretest_stress(message: types.message, state: FSMContext):
    await pre_points_test_stress(user_id=message.from_user.id, username=message.from_user.username)
    await pre_answers_test_stress(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_stress(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Тест на стрессоустойчивость'
                           '\nСодержащиеся в тесте симптомы стресса могут послужить предупреждением, особенно если они проявляются у вас довольно часто.'
                           '\n Приступим к тесту!', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await bot.send_message(message.from_user.id, text=questionstr[0], reply_markup=answers)
    db_stress = sqlite3.connect('Databases/Result_Tests/PSY_stress.db')
    cur_stress = db_stress.cursor()
    cur_stress.execute("UPDATE answers SET countOfAnswers = 0 WHERE user_id = ?", (message.from_user.id,))

async def answer_stress(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data[-1]
    db_stress = sqlite3.connect('Databases/Result_Tests/PSY_stress.db')
    cur_stress = db_stress.cursor()
    cur_answer_count = cur_stress.execute("SELECT countOfAnswers FROM answers WHERE user_id = ?",
                                             (callback_query.from_user.id,)).fetchone()
    str_to_execute = f"UPDATE answers SET answer{str(int(cur_answer_count[0]) + 1)} = ?"
    cur_stress.execute(str_to_execute, (point,))
    one = int(1)
    cur_stress.execute("UPDATE answers SET countOfAnswers = countOfAnswers + ? WHERE user_id = ?",
                         (one, callback_query.from_user.id))
    db_stress.commit()
    two = int(2)
    zero = int(0)
    check = cur_stress.execute("SELECT answer12 FROM answers WHERE user_id = ?",
                                  (callback_query.from_user.id,)).fetchone()
    print(check)
    cur_stress.execute(
        "UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if point == 'n':
        cur_stress.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (zero, callback_query.from_user.id))
    elif point == 'y':
        cur_stress.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [1, 2, 3, 5, 6, 8, 9, 10, 12, 14, 15, 16, 17, 18, 19, 21, 25, 26, 28, 29, 31, 32, 33]) and (point == 'm'):
        cur_stress.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    elif (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [20, 22, 23, 24, 27, 30]) and (point == 'm'):
        cur_stress.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [4, 7, 11, 13]) and (point == 'm'):
        cur_stress.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (zero, callback_query.from_user.id))
    db_stress.commit()
    if (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 33) and (point == 'y'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=questionstr[int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    elif (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 33) and (point == 'm'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=questionstr[int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    elif (int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 33) and (point == 'n'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=questionstr[int(cur_stress.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        await bot.send_message(callback_query.from_user.id, text='Ваш результат:')
        if int(cur_stress.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 12:
            await FSM_classes.MultiDialog.menu.set()
            munebut = InlineKeyboardMarkup(row_width=1)
            munebut.add(InlineKeyboardButton(
                'Вернуться в меню', callback_data='Main_menu'))
            await bot.send_message(callback_query.from_user.id, 'Результаты показывают, что Вы можете радоваться своей относительно здоровой стрессовой устойчивости. Если вы в данный момент прибегнете к мерам по преодолению стресса, то они, в первую очередь, будут иметь для вас профилактическое значение. Вы можете ожидать, что ваши недомогания, если они вообще есть, постепенно пойдут на убыль или вовсе исчезнут.', reply_markup=munebut)
            cur_stress.execute("UPDATE answers SET countOfAnswers = 0")
            db_stress.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_stress')
        elif (int(cur_stress.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 12) and (int(cur_stress.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 27):
            munebut = InlineKeyboardMarkup(row_width=1)
            munebut.add(InlineKeyboardButton(
                'Вернуться в меню', callback_data='Main_menu'))
            await bot.send_message(callback_query.from_user.id, 'Результаты показывают, что У вас уже проявляются цепные реакции физических и умственно-психических нарушений. Вам необходимо как можно скорее начать использовать в повседневной жизни упражнения по преодолению стресса. Уже через несколько недель в вашем состоянии наступит заметное улучшение благодаря ослаблению стрессовых симптомов или их снятию, а также повысится работоспособность.', reply_markup=munebut)
            cur_stress.execute("UPDATE answers SET countOfAnswers = 0")
            db_stress.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_stress')
        elif (int(cur_stress.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 27) and (int(cur_stress.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 66):
            munebut = InlineKeyboardMarkup(row_width=1)
            munebut.add(InlineKeyboardButton(
                'Вернуться в меню', callback_data='Main_menu'))
            cur_stress.execute("UPDATE answers SET countOfAnswers = 0")
            db_stress.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_stress')
        await bot.send_message(callback_query.from_user.id, 'Результаты показывают, что Вы глубоко увязли в замкнутом круге чрезмерных напряжений, чувствительных нагрузок и заметного расстройства здоровья. Вы должны предпринять какие-то целенаправленные действия против одолевающего вас стресса, чтобы тем самым вернуть себе спокойствие, уверенность, работоспособность.', reply_markup=munebut)


def register_handlers_Psy_stress(dp: Dispatcher):
    dp.register_callback_query_handler(
        answer_stress, text=['answer_y', 'answer_m', 'answer_n'])
