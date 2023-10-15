from PsyTests import Psy_Weariness, Psy_selfefficacy
from AllCourses import Anxiety
from Habits import Sleep, Water, Reading, Body
from PopTests import Pop_Control, Pop_Typeperson
from PsyTests import Psy_Weariness, Psy_selfefficacy, Psy_stress
import Specialists
import Habit
import Tests
import Courses
import Practices
import Markups
import FSM_classes
import asyncio
import sqlite3
from datetime import datetime, timedelta
import admin_commands
import quick_help
import Specialists

from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule as schedule

from aiogram.utils.exceptions import BotBlocked

from Token import Token
from Database import db_start, data_profile, affirmation, pre_points_test_weariness, points_test_weariness, pre_answers_test_weariness


async def on_startup(_):
    await db_start()


bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


Specialists.register_handlers_specialist(dp)
Psy_selfefficacy.register_handlers_Psy_selfefficacy(dp)
quick_help.register_handlers_quick_help(dp)
Psy_stress.register_handlers_Psy_stress(dp)
Pop_Control.register_handlers_Pop_Control(dp)
Pop_Typeperson.register_handlers_Pop_typeperson(dp)


@dp.message_handler(commands=['admin_mailing'], state='*', chat_id=417986886)
async def check_active_users(message: types.Message):
    await FSM_classes.Admin.mailing_all.set()
    await bot.send_message(message.from_user.id, text='Здравствуйте, босс! Пришлите то, что хотите разослать!',
                           parse_mode='html')


@dp.callback_query_handler(state=FSM_classes.MultiDialog.quick_help)
async def inline_quick_help(callback_query: types.CallbackQuery):
    await quick_help.all_way_callback_quick_help(callback_query)


@dp.message_handler(state=FSM_classes.MultiDialog.quick_help)
async def reply_quick_help(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await quick_help.all_way_quick_help(message)



@dp.message_handler(commands=['getuserreport'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите пароль:')
    await FSM_classes.adminCommands.getUserReportPassword.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportPassword)
async def get_user_report(message: types.Message, state: FSMContext):
    if message.text == 'admin123':
        await bot.send_message(message.from_user.id, text='Введите id нужных юзеров через пробел')
        await FSM_classes.adminCommands.getUserReportId.set()
    else:
        await bot.send_message(message.from_user.id, text='Ошибка доступа!'
                                                          '\n/getuserreport - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportId )
async def get_user_report(message: types.Message, state: FSMContext):
    await state.set_data({"users": message.text})
    await bot.send_message(message.from_user.id, text='Введите дату начала и конца наблюдений через пробел')
    await FSM_classes.adminCommands.getUserReportDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportDate)
async def get_user_report(message: types.Message, state: FSMContext):
    users = await state.get_data("users")
    startDate, endDate = message.text.split(' ')
    startDate = startDate.replace(':','')
    endDate = endDate.replace(':','')
    users = str(users['users']).split(' ')
    await admin_commands.createExcelFileReportCommand(startDate,endDate,users)
    with open('userData.xlsx', 'rb') as f:
        await bot.send_document(chat_id=message.from_user.id, document=InputFile(f))


@dp.message_handler(commands=['getuseractions'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите пароль:')
    await FSM_classes.adminCommands.getUserActionPassword.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionPassword)
async def get_user_report(message: types.Message, state: FSMContext):
    if message.text == 'admin123':
        await bot.send_message(message.from_user.id, text='Введите id нужных юзеров через пробел')
        await FSM_classes.adminCommands.getUserActionId.set()
    else:
        await bot.send_message(message.from_user.id, text='Ошибка доступа!'
                                                          '\n/getuserreport - ввести другой пароль '
                                                          '\n/main_menu - перейти в главное меню')


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionId)
async def get_user_report(message: types.Message, state: FSMContext):
    await state.set_data({"users": message.text})
    await bot.send_message(message.from_user.id, text='Введите дату начала и конца наблюдений через пробел')
    await FSM_classes.adminCommands.getUserActionDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserActionDate)
async def get_user_report(message: types.Message, state: FSMContext):
    users = await state.get_data("users")
    startDate, endDate = message.text.split(' ')
    users = str(users['users']).split(' ')
    await admin_commands.createExcelFileActionCommand(startDate,endDate,users)
    with open('getUserAction.xlsx', 'rb') as f:
        await bot.send_document(chat_id=message.from_user.id, document=InputFile(f))


@dp.message_handler(commands=['getuserreportgraph'], state='*')
async def get_user_report(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите дату формата чч:мм:гггг')
    await FSM_classes.adminCommands.getUserReportGraphDate.set()


@dp.message_handler(state=FSM_classes.adminCommands.getUserReportGraphDate)
async def get_user_report(message: types.Message, state: FSMContext):
    try:
        dateStart = datetime.strptime(message.text, '%d:%m:%Y')
        await bot.send_message(message.from_user.id, text='График вашего приема воды',reply_markup=Markups.backHabitRe)
        with open("scatter_plot.png", "rb") as f:
            photo = InputFile(f)
            await bot.send_photo(message.from_user.id, photo)
        await admin_commands.createGraphReportCommand(dateStart,message.from_user.id)
        await FSM_classes.MultiDialog.menu.set()
    except ValueError:
        await bot.send_message(message.from_user.id, text='Введена не корректная дата!\n'
                                                          'Введите дату в формате чч:мм:гггг')
        await FSM_classes.adminCommands.getUserReportGraphDate.set()



@dp.message_handler(content_types=['photo'], state=FSM_classes.Admin.mailing_all)
async def mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='mailing.jpg')
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await FSM_classes.MultiDialog.menu.set()
    for user in range(len(users)):
        try:
            photo_mailing = open('mailing.jpg', 'rb')
            await bot.send_photo(chat_id=(users[user][0]), photo=photo_mailing, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute(
                'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            db_user_blocked.commit()


@dp.message_handler(content_types=['text'], state=FSM_classes.Admin.mailing_all)
async def mailing_text(message: types.Message):
    db_user_blocked = sqlite3.connect('Databases/Data_users.db')
    cur_user_blocked = db_user_blocked.cursor()
    users = cur_user_blocked.execute('SELECT user_id FROM profile').fetchall()
    await FSM_classes.MultiDialog.menu.set()
    for user in range(len(users)):
        try:
            await bot.send_message(chat_id=(users[user][0]),
                                   text=message.text, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_user_blocked.execute(
                'UPDATE profile SET active = "Нет" WHERE user_id = ?', (users[user][0],))
            db_user_blocked.commit()


@dp.message_handler(commands=['start'], state='*')
async def welcome(message: types.Message):
    await data_profile(user_id=message.from_user.id, first_name=message.from_user.first_name,
                       username=message.from_user.username)
    await FSM_classes.MultiDialog.menu.set()
    Welcome_kb = InlineKeyboardMarkup()
    Welcome_kb.add(InlineKeyboardButton(
        'Приятно познакомиться!', callback_data='Welcome_btn0'))
    mess = f'Здравствуйте 🖐, <b>{message.from_user.first_name}</b>! Рад, что вы заботитетсь о своем ментальном здоровье! ' \
           f'\nБот Reform - это цифровой помощник, к которому вы сможете обратиться в случае возникновения стресса, тревоги или апатии, а самое главное для того, чтобы не допустить этого!' \
           f'\n\nОн поможет вам разобраться в проблеме и предоставит инструменты для её решения.' \
           f'\nВы сможете преодолеть любые преграды на вашем пути, а бот поможет вам советом и рекомендацией в трудную минуту!'
    await bot.send_message(message.from_user.id, mess, parse_mode='html', reply_markup=Welcome_kb)
    await log_users(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Welcome_btn'), state=FSM_classes.MultiDialog.menu)
async def mailing(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data[-1] == '0':
        enterIn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
            KeyboardButton('Чувствую проблему'),
            KeyboardButton('Пройти тест'))
        await bot.send_message(callback_query.from_user.id,
                               'Как вы себя чувствуете?'
                               '\n\nНажмите "Чувствую проблему", чтобы мгновенно получить рекомендации, которые помогут вам справиться с текущим состоянием '
                               'или нажмите "Пройти тест" для того, чтобы пройти текущему состоянию или пройти тест, состоящий из 36 вопросов для того, чтобы начать '
                               'наше знакомство и получить индивидуальную подборку рекомендаций, упражнений и практик для улучшения состояния!',
                               parse_mode='html', reply_markup=enterIn)


@dp.message_handler(commands=['main_menu'], state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await FSM_classes.HabitSleep.none.set()
    await FSM_classes.MultiDialog.menu.set()
    await bot.send_message(message.from_user.id, 'Вы в главном меню! Не знаете, что делать дальше?'
                                                 '\n\n🧘‍♀️ Практики помогут вам разгрузиться после тяжёлого дня или успокоиться'
                                                 '\n📝 Пройдите тесты, чтобы определить актуальное состояние и выявить проблему'
                                                 '\n💪 Трекер привычек поможет внедрить и поддерживать полезные навыки'
                                                 '\n🎬 Проходите курсы, узнавайте лучше себя, что поможет вам справиться с жизненными трудностями'
                                                 '\n💬 Также вы можете обсудить проблему и получить рекомендации от специалиста'
                                                 '\nВыберите, что вас интересует',
                           parse_mode='html', reply_markup=Markups.main_kb)
    await log_users(message)


@dp.message_handler(commands=['practices'], state='*')
async def practices(message: types.Message):
    await FSM_classes.MultiDialog.practices.set()
    await Practices.type_practices(message)


@dp.message_handler(commands=['test'], state='*')
async def test(message: types.message, state: FSMContext):
    await FSM_classes.MultiDialog.tests.set()
    await Tests.pretest(message, state)
    await log_users(message)


@dp.message_handler(commands=['courses'], state='*')
async def courses(message: types.Message, state: FSMContext):
    await FSM_classes.MultiDialog.courses.set()
    await Courses.precourse(message, state)
    await log_users(message)


@dp.message_handler(commands=['contacts'], state='*')
async def contacts(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте! '
                                                 'Меня зовут Reform. Я оказываю психологическую поддержку.'
                                                 'Мои возможности пока что ограничены, но меня совершенствуют с каждым днём.'
                                                 'Если у вас есть вопросы или вы обнаружили ошибку, вы можете обратиться к @APecherkin.',
                           parse_mode='html', reply_markup=Markups.cont)
    await log_users(message)


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('fullversion'), state=FSM_classes.MultiDialog)
# async def fullversion_callback(callback_query: types.CallbackQuery, state: FSMContext):
#     await bot.send_message(callback_query.from_user.id, 'Полный доступ доступен в платной версии.'
#                                                         '\nВ платной версии:'
#                                                         '❇️25 медитаций'
#                                                         '❇️10 дыхательных практик'
#                                                         '❇️Таймер Помодоро'
#                                                         '❇️Система ежедневных напоминаний и мотиваций'
#                                                         '❇️Рекомендации по сну, питанию и отдыху от ведущих специалистов'
#                                                         '\n\nОформить подписку за 499 рублей в месяц?',
#                            parse_mode='html')
#

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('Main_menu'), state='*')
async def main_menu_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await FSM_classes.HabitSleep.none.set()
    await FSM_classes.MultiDialog.menu.set()
    await bot.send_message(callback_query.from_user.id, 'Вы в главном меню. Не знаете что делать дальше?'
                                                        '\n\n🧘‍♀️ Практики помогут вам разгрузиться после тяжёлого дня или успокоиться'
                                                        '\n📝 Пройдите тесты, чтобы определить актуальное состояние и выявить проблему'
                                                        '\n💪 Трекер привычек поможет внедрить и поддерживать полезные навыки'
                                                        '\n🌳 Чувствуете себя не очень? Разберитесь поподробнее в себе и выявите проблему'
                                                        '\n💬 Также вы можете обсудить проблему и получить рекомендации от специалиста'
                                                        '\nВыберите, что вас интересует',
                           parse_mode='html', reply_markup=Markups.main_kb)


@dp.message_handler(state=FSM_classes.MultiDialog.practices)
async def reply_practices(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Practices.allreply_practices(message)
    await log_users(message)

@dp.message_handler(state=FSM_classes.MultiDialog.specialist)
async def reply_specialist(message: types.Message, state: FSMContext):
    if message.text == 'Перейти':
        await Specialists.choose_specialist(message, state)
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await Specialists.test_holms(message, state)
    await log_users(message)

@dp.message_handler(state=FSM_classes.MultiDialog.tests)
async def reply_tests(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
    await Tests.type_test(message, state)
    await log_users(message)


@dp.message_handler(state=(
        FSM_classes.MultiDialog.test_weariness or FSM_classes.MultiDialog.test_control or FSM_classes.MultiDialog.test_selfefficacy or FSM_classes.MultiDialog.test_typeperson or FSM_classes.MultiDialog.test_stress))
async def reply_alltests(message: types.Message, state: FSMContext):
    if message.text == 'Прервать тест и выйти в меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
        await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.courses)
async def reply_courses(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в меню':
        await main_menu(message, state)
    await Courses.type_course(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.course_anxiety)
async def reply_anxiety(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в меню':
        await FSM_classes.MultiDialog.menu.set()
        await main_menu(message, state)
        await log_users(message)


@dp.callback_query_handler(state=FSM_classes.MultiDialog.course_anxiety)
async def reply_anxiety(callback_query: types.CallbackQuery, state: FSMContext):
    await Anxiety.Course_Anxiety(callback_query, state)


@dp.message_handler(state=FSM_classes.MultiDialog.habits)
async def reply_habits(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Habit.choose_habit(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitWater.choose_action)
async def reply_habit_water(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Water.choose_habit_action(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitWater.choose_amount_of_portion)
async def reply_habit_water(message: types.Message, state: FSMContext):
    await Water.choose_habit_water_portions(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitWater.choose_schedule)
async def reply_habit_water(message: types.Message, state: FSMContext):
    await Water.choose_habit_water_schedule(message, state)
    await log_users(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('answerWater'), state='*')
async def reply_habit_water(callback_query: types.CallbackQuery, state: FSMContext):
    await Water.answer_water_schedule(callback_query, state)
    await FSM_classes.MultiDialog.menu.set()
    await log_users(callback_query.message)


@dp.message_handler(state=FSM_classes.HabitSleep.choose_action)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Sleep.choose_habit_action(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitSleep.choose_wakeup)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    await Sleep.choose_habit_sleep_wakeup(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.HabitSleep.choose_bedtime)
async def reply_habit_sleep(message: types.Message, state: FSMContext):
    await Sleep.choose_habit_sleep_bedtime(message, state)
    await log_users(message)


@dp.message_handler(state=FSM_classes.MultiDialog.specialist)
async def reply_specialist(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
    await Specialists.choose_specialist(message, state)
    await log_users(message)


@dp.message_handler(state='*')
async def reply_all(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню':
        await main_menu(message, state)
        await log_users(message)

    if message.text == 'Чувствую проблему':
        await FSM_classes.MultiDialog.quick_help.set()
        await bot.send_message(message.from_user.id, text='Выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее', reply_markup=quick_help.quick_help_menu)
        await log_users(message)
        await quick_help.all_way_quick_help(message)

    if message.text == 'Пройти тест':
        await FSM_classes.MultiDialog.test_weariness.set()
        await pre_points_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
        await pre_answers_test_weariness(user_id=message.from_user.id, username=message.from_user.username)
        async with state.proxy() as data:
            data['count'] = 0
        async with state.proxy() as data:
            data['points'] = 0
        await points_test_weariness(state, user_id=message.from_user.id)
        await state.finish()
        await bot.send_message(message.from_user.id, text=Psy_Weariness.weariness_questions[0], reply_markup=Psy_Weariness.answers)
        db_weariness = sqlite3.connect('Databases/Result_Tests/PSY_Weariness.db')
        cur_weariness = db_weariness.cursor()
        cur_weariness.execute("UPDATE answers SET countOfAnswers = 0 WHERE user_id = ?", (message.from_user.id,))
        db_weariness.commit()

    if message.text == '🧘‍♀️ Практики':
        await FSM_classes.MultiDialog.practices.set()
        await Practices.type_practices(message)
        await log_users(message)

    if message.text == '📝 Тесты':
        await FSM_classes.MultiDialog.tests.set()
        await Tests.pretest(message, state)
        await log_users(message)

    if message.text == '💪 Мои привычки':
        await FSM_classes.MultiDialog.habits.set()
        await Habit.prehabits(message, state)
        await log_users(message)

    if message.text == '🌳 Самоанализ':
        await FSM_classes.MultiDialog.quick_help.set()
        await bot.send_message(message.from_user.id,
                               text='Выберите, что вы чувствуете, чтобы разобраться в проблеме поподробнее',
                               reply_markup=quick_help.quick_help_menu)
        await log_users(message)
        await quick_help.all_way_quick_help(message)
        await log_users(message)

    if message.text == '💬 Обсудить проблему':
        await FSM_classes.MultiDialog.specialist.set()
        await Specialists.choose_specialist(message, state)
        await log_users(message)

    if message.text == '📥 Контакты':
        await contacts(message)
        await log_users(message)

    if message.text == 'Что ты умеешь?':
        back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Вернуться в главное меню')
        back.add(btn1)
        await bot.send_message(message.from_user.id,
                               'Я могу оценить ваше состояние и подобрать индивидуальные упражнения, которые помогут справиться с психологическими проблемами. '
                               '\n\nВыберите раздел с практиками, если хотите разгрузиться или чувствуете себя не важно. '
                               '\nВ разделе с курсами вы можете углубиться в интересующую вас проблему и решить её с помощью специальных методик разработанных специалистами.'
                               '\nВ разделе музыка вы можете найти для себя подходящую мелодию и расслабиться'
                               '\nТакже, если вы не знаете в чём проблема, но чувствуете себя не очень, то можете пройти тесты и лучше понять себя'
                               '\n\n Приятного использования и жизни в гармонии со своим ментальным здоровьем!',
                               parse_mode='html', reply_markup=back)
        await log_users(message)


@dp.channel_post_handler(content_types=['text'])
async def affirmation_mailing_text(message: types.Message):
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users_affirmation = cur_data.execute(
        'SELECT user_id FROM affirmation').fetchall()
    for user_miling in range(len(users_affirmation)):
        try:
            await bot.send_message(chat_id=(users_affirmation[user_miling][0]),
                                   text=message.text, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE affirmation SET user_id = 0 WHERE user_id = ?',
                             (users_affirmation[user_miling][0],))
            db_data.commit()
    cur_data.execute('DELETE FROM affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()


@dp.channel_post_handler(content_types=['photo'])
async def affirmation_mailing_photo(message: types.Message):
    await message.photo[-1].download(destination_file='affirmation.jpg')
    db_data = sqlite3.connect('Databases/Data_users.db')
    cur_data = db_data.cursor()
    users_affirmation = cur_data.execute(
        'SELECT user_id FROM affirmation').fetchall()
    await asyncio.sleep(1)
    for user_miling in range(len(users_affirmation)):
        try:
            photo = open('affirmation.jpg', 'rb')
            await bot.send_photo(chat_id=(users_affirmation[user_miling][0]),
                                 photo=photo, parse_mode='html')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_data.execute('UPDATE affirmation SET user_id = 0 WHERE user_id = ?',
                             (users_affirmation[user_miling][0],))
            db_data.commit()
    cur_data.execute('DELETE FROM affirmation WHERE user_id = ?', (int(0),))
    db_data.commit()


async def scheduler_sleep_message_wakeup():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_wakeup = cur_scheduler.execute(
        'SELECT user_id FROM sleep WHERE wakeup = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_wakeup in range(len(users_wakeup)):
        try:
            await bot.send_message(chat_id=users_wakeup[user_wakeup][0], text='Пора вставать! '
                                                                              '\nНачинать никогда не поздно! А всё начинается с небольших изменений!')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_scheduler.execute(
                'UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_wakeup[user_wakeup][0],))
            db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()


async def scheduler_sleep_message_bedtime():
    db_scheduler_sleep = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler = db_scheduler_sleep.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    users_bedtime = cur_scheduler.execute(
        'SELECT user_id FROM sleep WHERE bedtime = ?', (now.strftime('%H:%M'),)).fetchall()
    for user_bedtime in range(len(users_bedtime)):
        try:
            await bot.send_message(chat_id=users_bedtime[user_bedtime][0],
                                   text='Вы просили напомнить, что вам пора ложиться спать!'
                                        '\nЗавтра вас ждёт отличный день! '
                                        '\nПомните, великое начинется с малого!')
            await asyncio.sleep(0.1)
        except BotBlocked:
            cur_scheduler.execute(
                'UPDATE sleep SET user_id = 0 WHERE user_id = ?', (users_bedtime[user_bedtime][0],))
            db_scheduler_sleep.commit()
    cur_scheduler.execute('DELETE FROM sleep WHERE user_id = ?', (int(0),))
    db_scheduler_sleep.commit()


async def scheduler_water_message():
    db_scheduler_water = sqlite3.connect('Databases/Current_habits.db')
    cur_scheduler_water = db_scheduler_water.cursor()
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    time_in_min_now = int(now.strftime('%H:%M').split(':')[0]) * 60 + int(now.strftime('%H:%M').split(':')[1])
    today = datetime.today()
    weekday = today.weekday()

    if weekday < 5:
        users = cur_scheduler_water.execute(
            'SELECT user_id FROM water WHERE interval != 0 AND schedule IN ("weekdays", "both")').fetchall()
    if weekday >= 5:
        users = cur_scheduler_water.execute(
            'SELECT user_id FROM water WHERE interval != 0 AND schedule IN ("weekends", "both")').fetchall()

    if time_in_min_now in range(600, 1381):
        for user in users:
            interval = cur_scheduler_water.execute(
                'SELECT interval FROM water WHERE user_id = ?', (user[0],)).fetchone()
            amount_of_portions = cur_scheduler_water.execute(
                'SELECT amountOfPortions FROM water WHERE user_id = ?', (user[0],)).fetchone()

            if time_in_min_now % interval[0] == 0:
                try:
                    await bot.send_message(chat_id=user[0], text='Пора пить воду!'
                                                                 '\nОбъем приёма воды - ' + str(
                        round(2000 / amount_of_portions[0])) + ' мл.')
                    await asyncio.sleep(0.1)
                except BotBlocked:
                    cur_scheduler_water.execute(
                        'UPDATE water SET user_id = 0 WHERE user_id = ?', (users[user[0]][0],))
                    db_scheduler_water.commit()
                cur_scheduler_water.execute('DELETE FROM water WHERE user_id = ?', (int(0),))
                db_scheduler_water.commit()
            if time_in_min_now == 1380:
                today = datetime.today()
                tableName = 'date_' + str(today)[0:10].replace('-', '')
                cur_scheduler_water.execute(f'ALTER TABLE waterDates ADD COLUMN {tableName} TEXT')
                await bot.send_message(chat_id=user[0], text='Получилось ли выполнить норму?',
                                       reply_markup=Markups.waterAnswers)


async def scheduler_sleep():
    schedule.every(1).minute.do(scheduler_sleep_message_wakeup)
    schedule.every(1).minute.do(scheduler_sleep_message_bedtime)
    now = datetime.utcnow() + timedelta(hours=3, minutes=0)
    time_in_min_now = int(now.strftime('%H:%M').split(':')[0]) * 60 + int(now.strftime('%H:%M').split(':')[1])
    if time_in_min_now >= 600 and time_in_min_now <= 1380:
        schedule.every(1).minute.do(scheduler_water_message)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)


async def log_users(message: types.Message):
    now = datetime.now()
    botlogfile = open('LogsBot', 'a')
    print(now.strftime('%d-%m-%Y %H:%M'), ' Пользователь - ' + message.from_user.first_name,
          message.from_user.id, 'Написал - ' + message.text, file=botlogfile)
    botlogfile.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_sleep())
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
