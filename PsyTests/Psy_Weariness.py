from datetime import datetime

import FSM_classes
import Markups
from Database import db_start, data_profile, pre_points_test_weariness, points_test_weariness, pre_answers_test_weariness,save_user_action
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


weariness_questions = ["Чаще всего у меня хорошее самочувствие",
                       "Я стал(а) раздражительным",
                       "В последнее время я стал(а) хуже видеть",
                       "Я стал(а) забывчивым",
                       "После работы я чувствую себя разбитым(ой)",
                       "Мне нравится работать в коллективе",
                       "У меня часто бывает подавленное настроение",
                       "Я чувствую постоянную тяжесть в голове",
                       "У меня отекают ноги",
                       "У меня бывают головокружения",
                       "У меня бывает ощущение, что мне трудно вздохнуть",
                       "Мне всегда хочется как можно быстрее закончить работу и уйти домой",
                       "После сна я обычно встаю вялым(ой) и плохо отдохнувшим(ей)",
                       "Мой рабочий день обычно пролетает незаметно",
                       "Я стал(а) часто ссориться со своими близкими",
                       "После пробуждения я засыпаю с трудом",
                       "Я постоянно испытываю неприятные ощущения в глазах",
                       "В последнее время меня стали раздражать те дела, которые нужно сделать сегодня",
                       "Я стал(а) вялым и безразличным",
                       "Мне трудно удержать в памяти те дела, которые нужно сделать сегодня",
                       "В последнее время мне стало трудно работать",
                       "У меня ровный и спокойный характер",
                       "Меня мучают боли в висках и во лбу",
                       "У меня часто бывают приступы сердцебиения",
                       "Когда я работаю, у меня почти все время болят спина и шея",
                       "У меня часто возникает ощущение тошноты",
                       "У меня часто болит голова",
                       "Моя работа мне перестала нравиться",
                       "Я постоянно хочу спать днем",
                       "Мои близкие стали замечать, что у меня портится характер",
                       "Когда я читаю, мне приходится напрягать глаза",
                       "Чаще всего у меня беспокойный сон",
                       "Я с удовольствием прихожу на работу",
                       "Я все время чувствую себя усталым(ой)",
                       "В последнее время я чувствую общее недомогание",
                       "Я чувствую себя абсолютно здоровым человеком"]


answers = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='Answer_y'),
                                     InlineKeyboardButton(
                                         'Не уверен(а)', callback_data='Answer_m'),
                                     InlineKeyboardButton('Нет', callback_data='Answer_n'))


async def pretest_weariness(message: types.message, state: FSMContext):
    await pre_points_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
    await pre_answers_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_weariness(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Хроническое утомление даже на ранних стадиях развития существенно снижает работоспособность человека, '
                           'а в выраженных степенях приводит к затруднению выполнения даже хорошо знакомой работы '
                           'и в крайних степенях – к полному срыву деятельности. '
                           '\n Чтобы этого избежать, предлагаем вам пройти небольшой тест, чтобы оценить ваш уровень утомляемости и подобрать для вас нужные рекомендации и практики. '
                           '\nВам будет представлены высказывания, отвечайте "Да", если это про вас, "Нет", если не про вас, и "Не уверен(а)", если затрудняетесь ответить.'
                           '\n Приступим к тесту!', reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await bot.send_message(message.from_user.id, text=weariness_questions[0], reply_markup=answers)
    db_weariness = sqlite3.connect('Databases/Result_Tests/PSY_Weariness.db')
    cur_weariness = db_weariness.cursor()
    cur_weariness.execute("UPDATE answers SET countOfAnswers = 0 WHERE user_id = ?", (message.from_user.id,))
    db_weariness.commit()

async def answer_weariness(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data[-1]
    one = int(1)
    two = int(2)
    db_weariness = sqlite3.connect('Databases/Result_Tests/PSY_Weariness.db')
    cur_weariness = db_weariness.cursor()
    cur_answer_count = cur_weariness.execute("SELECT countOfAnswers FROM answers WHERE user_id = ?", (callback_query.from_user.id,)).fetchone()
    str_to_execute = f"UPDATE answers SET answer{str(int(cur_answer_count[0])+1)} = ?"
    cur_weariness.execute(str_to_execute, (point,))
    cur_weariness.execute("UPDATE answers SET countOfAnswers = countOfAnswers + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    db_weariness.commit()
    cur_weariness.execute(
        "UPDATE points SET count = (count + ?) WHERE user_id = ?", (one, callback_query.from_user.id))
    if (int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [1, 6, 14, 22, 33, 36]) and (point == 'n'):
        cur_weariness.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif (int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) in [2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35]) and (point == 'y'):
        cur_weariness.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (two, callback_query.from_user.id))
    elif point == 'm':
        cur_weariness.execute(
            "UPDATE points SET points = points + ? WHERE user_id = ?", (one, callback_query.from_user.id))
    db_weariness.commit()
    if (int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 36) and (point == 'y'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=weariness_questions[int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    elif (int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 36) and (point == 'm'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=weariness_questions[int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    elif (int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) != 36) and (point == 'n'):
        await bot.edit_message_text(chat_id=callback_query.from_user.id, text=weariness_questions[int(cur_weariness.execute('SELECT count FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0])], message_id=callback_query.message.message_id, reply_markup=answers)
    else:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if int(cur_weariness.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 17:
            await FSM_classes.MultiDialog.menu.set()
            await bot.send_message(callback_query.from_user.id, 'Результаты показывают, что у вас отсутствуют признаки хронического утомления. Надеемся, что текущая работа и дальше будет вам интересна и желанна', reply_markup=Markups.backIn)
            cur_weariness.execute("UPDATE answers SET countOfAnswers = 0")
            db_weariness.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Weariness')
        elif (int(cur_weariness.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 17) and (int(cur_weariness.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 26):
            Feedback_kb = InlineKeyboardMarkup(row_width=1)
            Feedback_kb.add(InlineKeyboardButton('Посмотреть курс', callback_data='Feedback_btn0'),
                            InlineKeyboardButton('Вернуться в меню', callback_data='Main_menu'))
            await bot.send_message(callback_query.from_user.id, 'Результаты показывают, что у вас присутствуют признаки начальной степени хронического утомления. Рекомендуем вам пройти небольшой курс поддерживающих практик', reply_markup=Feedback_kb)
            cur_weariness.execute("UPDATE answers SET countOfAnswers = 0")
            db_weariness.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Weariness')
        elif (int(cur_weariness.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) > 26) and (int(cur_weariness.execute('SELECT points FROM points WHERE user_id = ?', (callback_query.from_user.id,)).fetchone()[0]) <= 37):
            Feedback_kb = InlineKeyboardMarkup(row_width=1)
            Feedback_kb.add(InlineKeyboardButton('Посмотреть курс', callback_data='Feedback_btn0'),
                            InlineKeyboardButton('Вернуться в меню', callback_data='Main_menu'))
            await bot.send_message(callback_query.from_user.id,
                                   'Результаты показывают, что у вас присутствуют признаки выраженной степени хронического утомления. Рекомендуем вам пройти небольшой курс восстанавливающих и поддерживающих практик', reply_markup=Feedback_kb)
            cur_weariness.execute("UPDATE answers SET countOfAnswers = 0")
            db_weariness.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Weariness')
        else:
            await FSM_classes.MultiDialog.specialist.set()
            Feedback_kb = InlineKeyboardMarkup(row_width=1)
            Feedback_kb.add(InlineKeyboardButton('Перейти к практикам', callback_data='Feedback_btn0'),
                            InlineKeyboardButton('Хочу обратиться к специалисту', callback_data='Feedback_btn6'))
            await bot.send_message(callback_query.from_user.id,
                                   'Результаты показывают, что у вас присутствуют признаки сильной степени хронического утомления. Рекомендуем вам пройти курс восстанавливающих и поддерживающих практик а также обратиться к специалисту в ближайшее время', reply_markup=Feedback_kb)
            cur_weariness.execute("UPDATE answers SET countOfAnswers = 0")
            db_weariness.commit()
            await save_user_action(user_id=callback_query.from_user.id, action='Psy_Weariness')

async def process_callback_feedback(callback_query: types.CallbackQuery, state: FSMContext):
    point = callback_query.data[-1]
    if point == '0':
        # async with state.proxy() as data:
        #     data['aftertest1'] = 'Перешёл'
        #     data['aftertest2'] = '-'
        #     data['aftertest3'] = '-'
        Feedback_kb = InlineKeyboardMarkup()
        Feedback_kb.add(InlineKeyboardButton(
            'Начать практику', callback_data='Feedback_btn1'))
        await bot.send_message(callback_query.from_user.id,
                               'Предлагаем вам простую технику «Дыхание квадрат». '
                               'Оно позволит растянуть дыхательный цикл и с помощью этого увеличить содержание углекислого газа в крови и разгрузить вашу нервную систему.'
                               'Лучше всего удобно сесть, если нет возможности, то выберете положение, в котором вам комфортнее всего.'
                               'Попробуйте расслабиться и сконцентрироваться на дыхании', parse_mode='html', reply_markup=Feedback_kb)
    if point == '1':
        Feedback_kb = InlineKeyboardMarkup()
        Feedback_kb.add(InlineKeyboardButton(
            'Выполнено!', callback_data='Feedback_btn2'))
        await bot.send_message(callback_query.from_user.id,
                               "Вдох, выдох и пауза примерно равны друг другу по длительности, комфортный ритм – примерно 4 секунд")
        ExVisualAudio2 = open('Exercises/Дыхание квадрат.mp3', 'rb')
        photo = open('Exercises/Квадрат дыхания.jpg', 'rb')
        await bot.send_photo(callback_query.from_user.id, photo)
        await bot.send_audio(callback_query.from_user.id, ExVisualAudio2, reply_markup=Feedback_kb)
    if point == '2':
        Feedback_kb = InlineKeyboardMarkup()
        Feedback_kb.add(InlineKeyboardButton('Да', callback_data='Feedback_btn3'),
                        InlineKeyboardButton('Нет', callback_data='Feedback_btn4'))
        await bot.send_message(callback_query.from_user.id,
                               "Советуем вам выполнять практики вечером, после работы. "
                               "\nЭто позволит вам эффективно разгрузить нервную систему и сбросить напряжение. "
                               "\nВам бы хотелось выбрать удобное время для напоминаний?", reply_markup=Feedback_kb)
    if point == '3':
        # async with state.proxy() as data:
        #     data['aftertest4'] = 'Да'
        now = datetime.now()
        botlogfile = open('LogsBot', 'a')
        print(now.strftime('%d-%m-%Y %H:%M'), ' Пользователь - ' + callback_query.from_user.first_name,
              callback_query.from_user.id, 'Хочет получать напоминания по выполнению практик')
        botlogfile.close()
        Feedback_kb = InlineKeyboardMarkup(row_width=1)
        Feedback_kb.add(InlineKeyboardButton('Хочу посмотреть эти практики', callback_data='Feedback_btn5'),
                        InlineKeyboardButton('Перейти в меню', callback_data='Main_menud'))
        await bot.send_message(callback_query.from_user.id,
                               "Отлично! В скором времени такая возможность появиться! Мы вас оповестим!")
        await bot.send_message(callback_query.from_user.id,
                               "Чтобы чувствовать себя бодрым и эффективным, существует множество хороших привычек, "
                               "которые позволят держать в тонусе организм и сознание - внедрение правильного режима сна, физических упражнений, употребление нужного количесвта воды и другие",
                               reply_markup=Feedback_kb)

    if point == '4':
        # async with state.proxy() as data:
        #     data['aftertest4'] = 'Нет'
        Feedback_kb = InlineKeyboardMarkup(row_width=1)
        Feedback_kb.add(InlineKeyboardButton('Хочу посмотреть эти практики', callback_data='Feedback_btn5'),
                        InlineKeyboardButton('Перейти в меню', callback_data='Main_menu'))
        await bot.send_message(callback_query.from_user.id,
                               "Чтобы чувствовать себя бодрым и эффективным, существует множество хороших привычек, "
                               "которые позволят держать в тонусе организм и сознание - внедрение правильного режима сна, физических упражнений, употребление нужного количесвта воды и другие", reply_markup=Feedback_kb)
    if point == '5':
        await FSM_classes.MultiDialog.habits.set()
        await bot.send_message(callback_query.from_user.id,
                               'В этом разделе вы найдёте полезные практики и привычки, которые вы сможете внедрить в свою жизнь прямо сейчас.'
                               'Для этого вам всего лишь нужно выбрать интересующую и время напоминаний, но не забывайте, что самое главное - ваши старания!',
                               reply_markup=Markups.type_of_habits)
    if point =='6':
        spec = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Перейти'))
        await bot.send_message(callback_query.from_user.id, 'Вы хотите перейти на страницу записи к психотерапевту?', reply_markup=spec)
        await FSM_classes.MultiDialog.specialist.set()


def register_handlers_Psy_Weariness(dp: Dispatcher):
    dp.register_callback_query_handler(
        answer_weariness, text=['Answer_y', 'Answer_m', 'Answer_n'])
    dp.register_callback_query_handler(process_callback_feedback, text=[
                                       'Feedback_btn0', 'Feedback_btn1', 'Feedback_btn2', 'Feedback_btn3', 'Feedback_btn4', 'Feedback_btn5', 'Feedback_btn6'])
