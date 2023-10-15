from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
import sqlite3

from Database import db_start, data_profile, save_user_action, pre_points_test_holms, pre_answers_test_holms, points_test_holms
import FSM_classes
import Markups

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


async def choose_specialist(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.specialist.set()
    specialist_test = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Приступить к тесту'))
    await bot.send_message(message.from_user.id, 'Для того, чтобы подобрать вам подходящего психотерапевта и ускорить '
                                                 'процесс взаимодействия с ним, предлагаем вам пройти тест Холмса-Рея. '
                                                 '\n\nТест содержит список из 43 событий повседневной жизни, '
                                                 'имеющих различную эмоциональную окраску и значимость, каждое из которых оцениваетя в определенное количество баллов. '
                                                 '\nВам необходимо выбрать события, с которыми вы сталкивались за последний год.'
                                                 '\nОтвечайте "Да", если событие имело место в вашей жизни и "Нет", если этого не было (это займет не более 2-3 минут)', reply_markup=specialist_test)


holms_questions = ["Смерть супруга / супруги",
                   "Развод",
                   "Расставание супругов",
                   "Тюремное заключение",
                   "Смерть кого-то из близких",
                   "Несчастный случай, болезнь",
                   "Женитьба (замужество)",
                   "Увольнение с работы",
                   "Воссоединение супругов",
                   "Выход на пенсию",
                   "Ухудшение здоровья кого-то из близких",
                   "Беременность",
                   "Сексуальные затруднения",
                   "Пополнение семьи",
                   "Поступление па работу",
                   "Изменение материального положения",
                   "Смерть близкого друга / подруги",
                   "Переход па другую работу",
                   "Семейные ссоры стали чаще/реже",
                   "Долг свыше $10000",
                   "Возвращение долга / ссуды",
                   "Ответственность па службе повысилась/понизилась",
                   "Сын или дочь покидают семью",
                   "Ссора с родней мужа / жены",
                   "Успех",
                   "Жена идет работать / оставляет работу",
                   "Начало/конец школьных занятий",
                   "Изменения условий жизни",
                   "Изменение старых привычек",
                   "Неприятности с руководством па службе",
                   "Изменение продолжительности или условий работы",
                   "Перемена места жительства",
                   "Перемена школы",
                   "Перемена в развлечениях",
                   "Изменение в деятельности религиозного характера",
                   "Увеличение / снижение общественной активности",
                   "Долг менее $10000",
                   "Изменение привычек, связанных со сном",
                   "Семейные праздники отмечаются чаще / реже",
                   "Изменение режима питания",
                   "Каникулы / отпуск",
                   "Рождество",
                   "Незначительное нарушение закона"]

points_holms_questions = [100,73,65,63,63,53,50,47,45,45,44,40,39,39,39,39,37,36,35,31,30,29,29,29,28,26,26,25,24,23,20,20,20,19,19,18,17,16,15,15,13,12,11]


holms_answers = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='Answer_Y'), InlineKeyboardButton('Нет', callback_data='Answer_N'))


async def test_holms(message: types.message, state: FSMContext):
    if message.text == 'Приступить к тесту':
        await pre_points_test_holms(user_id=message.from_user.id, username=message.from_user.username)
        await pre_answers_test_holms(user_id=message.from_user.id, username=message.from_user.username)
        async with state.proxy() as data:
            data['count'] = 0
        async with state.proxy() as data:
            data['points'] = 0
        await points_test_holms(state, user_id=message.from_user.id)
        await state.finish()
        await bot.send_message(message.from_user.id, 'Начнём тест', reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id, text=holms_questions[0], reply_markup=holms_answers)
        db_holms = sqlite3.connect('Databases/Result_Tests/Holmes-Rahe.db')
        cur_holms = db_holms.cursor()
        cur_holms.execute("UPDATE answers SET countOfAnswers = 0 WHERE user_id = ?", (message.from_user.id,))
        db_holms.commit()
    if message.text == 'Записаться':
        await bot.send_message(message.from_user.id,
                               'Перейдите по ссылке для записи - https://dikidi.net/1046062?p=0.pi')
        await save_user_action(user_id=message.from_user.id, action='Перешел по ссылке на запись к психотерапевту')

async def answer_holms(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data[-1]
    one=int(1)
    db_holms = sqlite3.connect('Databases/Result_Tests/Holmes-Rahe.db')
    cur_holms = db_holms.cursor()
    cur_answer_count_ = cur_holms.execute("SELECT countOfAnswers FROM answers WHERE user_id = ?",
                                             (callback_query.from_user.id,)).fetchone()
    str_to_execute_ = f"UPDATE answers SET answer{str(int(cur_answer_count_[0]) + 1)} = ?"
    cur_holms.execute(str_to_execute_, (point,))
    cur_holms.execute("UPDATE answers SET countOfAnswers = countOfAnswers + ? WHERE user_id = ?",
                          (one, callback_query.from_user.id))
    db_holms.commit()
    if point == 'Y':
        cur_holms.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (points_holms_questions[int(
            cur_holms.execute('SELECT count FROM points WHERE user_id = ?',
                                  (callback_query.from_user.id,)).fetchone()[0])], callback_query.from_user.id))
    cur_holms.execute(
        "UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    db_holms.commit()

    if (int(cur_holms.execute('SELECT count FROM points WHERE user_id = ?',
                                  (callback_query.from_user.id,)).fetchone()[0]) != 43):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=holms_questions[int(
            cur_holms.execute('SELECT count FROM points WHERE user_id = ?',
                                  (callback_query.from_user.id,)).fetchone()[0])],
                                    message_id=callback_query.message.message_id, reply_markup=holms_answers)
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if int(cur_holms.execute('SELECT points FROM points WHERE user_id = ?',
                                     (callback_query.from_user.id,)).fetchone()[0]) < 150:
            await bot.send_message(callback_query.from_user.id,
                                   'Результаты показывают, что у вас низкий уровень стресса и низкая вероятность стрессовых расстройств. '
                                   '\n\n Мы подобрали для вас нужного психолога, для того, чтобы записаться, нажмите на кнопку '
                                   '"Записаться", переходите по ссылке на форму записи подобранного психолога и записывайтесь на удобное время',
                                   reply_markup=Markups.appointment)
            await FSM_classes.MultiDialog.menu.set()
            cur_holms.execute("UPDATE answers SET countOfAnswers = 0")
            db_holms.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Завершил тест Холмса-Рея (<150)')
            await FSM_classes.MultiDialog.specialist.set()
        elif (int(cur_holms.execute('SELECT points FROM points WHERE user_id = ?',
                                        (callback_query.from_user.id,)).fetchone()[0]) >= 150) and (int(
                cur_holms.execute('SELECT points FROM points WHERE user_id = ?',
                                      (callback_query.from_user.id,)).fetchone()[0]) < 300):
            await bot.send_message(callback_query.from_user.id,
                                   'Результаты показывают, что у вас есть риск развития расстройства около 50%.'
                                   '\n\n Мы подобрали для вас нужного психолога, для того, чтобы записаться, нажмите на кнопку '
                                   '"Записаться", переходите по ссылке на форму записи подобранного психолога и записывайтесь на удобное время',
                                   reply_markup=Markups.appointment)
            await FSM_classes.MultiDialog.menu.set()
            cur_holms.execute("UPDATE answers SET countOfAnswers = 0")
            db_holms.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Завершил тест Холмса-Рея (150-300)')
            await FSM_classes.MultiDialog.specialist.set()
        else:
            await bot.send_message(callback_query.from_user.id,
                                   'Результаты показывают, что ваш риск стрессового расстройства достиг 80%'
                                   '\n\n Мы подобрали для вас нужного психолога, для того, чтобы записаться, нажмите на кнопку '
                                   '"Записаться", переходите по ссылке на форму записи подобранного психолога и записывайтесь на удобное время',
                                   reply_markup=Markups.appointment)
            await FSM_classes.MultiDialog.menu.set()
            cur_holms.execute("UPDATE answers SET countOfAnswers = 0")
            db_holms.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Завершил тест Холмса-Рея (>300)')
            await FSM_classes.MultiDialog.specialist.set()

def register_handlers_specialist(dp: Dispatcher):
    dp.register_callback_query_handler(
        answer_holms, text=['Answer_Y', 'Answer_N'])
