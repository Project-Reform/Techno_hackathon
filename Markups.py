from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Main_menu
Practise_btn = KeyboardButton('🧘‍♀️ Практики')
Tests_btn = KeyboardButton('📝 Тесты')
Habits_btn = KeyboardButton('💪 Мои привычки')
Help_btn = KeyboardButton('🌳 Самоанализ')
Specialist_btn = KeyboardButton('💬 Обсудить проблему')
Contacts_btn = KeyboardButton('📥 Контакты')
main_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_kb.add(Help_btn, Practise_btn, Specialist_btn,
            Tests_btn, Habits_btn, Contacts_btn)

# Practices
Duh_btn = KeyboardButton('Дыхательные практики')
Med_btn = KeyboardButton('Медитативные практики')
Practice_kb = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
Practice_kb.add(Duh_btn, Med_btn)

endpractice = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn1 = KeyboardButton('Выбрать другую практику')
btn2 = KeyboardButton('Вернуться в главное меню')
endpractice.add(btn1, btn2)

# AllCourses
course1 = KeyboardButton('Борьба с тревогой')
course2 = KeyboardButton('Здоровый сон')
course3 = KeyboardButton('Бодрое утро')
course4 = KeyboardButton('Безмятежный вечер')
course5 = KeyboardButton('Эмоциональное выгорание')
course6 = KeyboardButton('Борьба с депрессией')
coursepv = KeyboardButton('Подробнее о полной версии')
courseback = KeyboardButton('Вернуться в главное меню')
courses_kb = ReplyKeyboardMarkup(row_width=1)
courses_kb.add(course1, course2, course3, course4,
               course5, course6, coursepv, courseback)

# Contacts
cont = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn1 = KeyboardButton('Что ты умеешь?')
btn2 = KeyboardButton('Вернуться в главное меню')
cont.add(btn1, btn2)

# Tests
typetest1 = KeyboardButton('Психологические тесты')
typetest2 = KeyboardButton('Популярные тесты')
typetestback = KeyboardButton('Вернуться в главное меню')
type_of_tests = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    typetest1, typetest2, typetestback)

psy_tests = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Хроническая усталость'),
    KeyboardButton('Устойчивость к стрессу'),
    KeyboardButton('Личная самоэффективность'),
    KeyboardButton('Психологическое благополучие (скоро)'),
    KeyboardButton('Доминирующее состояние (скоро)'))

pop_tests = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Управляю ли я своей жизнью?'),
    KeyboardButton('Мой тип личности'),
    KeyboardButton('Мой темперамент (скоро)'),
    KeyboardButton('Мои скрытые таланты и способности (скоро)'))

# Back to menu
backIn = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    InlineKeyboardButton('Вернуться в меню', callback_data='Main_menu'))

backRe = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Прервать тест и выйти в меню'))

backCourseRe = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Вернуться в меню', callback_data='Main_menu'))

# Full version
fullversion = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Оформить подписку'))

# Habits
type_of_habits = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Работа со сном'),
    KeyboardButton('Регулярное чтение книг (скоро)'),
    KeyboardButton('Дневная норма воды'),
    KeyboardButton('Работа с телом (скоро)'),
    KeyboardButton('Вернуться в главное меню'))

tune_habit = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Настроить привычку'),
    KeyboardButton('Удалить привычку'),
    KeyboardButton('Вернуться в главное меню'))

backHabitRe = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Вернуться в главное меню', callback_data='Main_menu'))


chooseScheduleWater = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Будние'),
    KeyboardButton('Выходные'),
    KeyboardButton('Вся неделя'))

waterAnswers = InlineKeyboardMarkup().add(
    InlineKeyboardButton('Получилось!',callback_data='answerWatery'),
    InlineKeyboardButton('К сожалению, нет.',callback_data='answerWatern'))

# Specialist
appointment = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Записаться'),
    KeyboardButton('Вернуться в главное меню'))

