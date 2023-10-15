from aiogram.dispatcher.filters.state import StatesGroup, State


class MultiDialog(StatesGroup):
    quick_help = State()
    menu = State()
    practices = State()
    tests = State()
    test_weariness = State()
    test_stress = State()
    test_temperament = State()
    test_selfefficacy = State()
    test_control = State()
    test_typeperson = State()
    habits = State()
    sleep_habit = State()
    water_habit = State()
    reading_habit = State()
    body_habit = State()
    courses = State()
    course_anxiety = State()
    specialist = State()



class HabitSleep(StatesGroup):
    none = State()
    choose_action = State()
    choose_bedtime = State()
    choose_wakeup = State()

class HabitWater(StatesGroup):
    none = State()
    choose_action = State()
    choose_amount_of_portion = State()
    choose_schedule = State()


class Admin(StatesGroup):
    mailing_all = State()


class adminCommands(StatesGroup):
    getUserReportPassword = State()
    getUserReport = State()
    getUserReportId = State()
    getUserReportDate = State()
    getUserActionPassword = State()
    getUserActionId = State()
    getUserActionDate = State()
    getUserReportGraphDate = State()
