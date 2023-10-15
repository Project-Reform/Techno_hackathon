from aiogram import Bot, types
from aiogram.dispatcher import FSMContext


from Token import Token
bot = Bot(Token)


import FSM_classes
import Markups
import Habits

async def prehabits(message: types.message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           'В этом разделе вы найдёте полезные практики и привычки, которые вы сможете внедрить в свою жизнь прямо сейчас. '
                           'Для этого вам всего лишь нужно выбрать интересующую и время напоминаний, но не забывайте, что самое главное - ваши старания!' ,reply_markup=Markups.type_of_habits)

async def choose_habit(message: types.message, state: FSMContext):
    if message.text == 'Работа со сном':
        await FSM_classes.MultiDialog.sleep_habit.set()
        await Habits.Sleep.habit_sleep(message, state)
    #
    # if message.text == 'Регулярное чтение книг':
    #     await FSM_classes.MultiDialog.test_selfefficacy.set()
    #     await PsyTests.Psy_selfefficacy.pretest_selfefficacy(message, state)
    #
    if message.text == 'Дневная норма воды':
        await FSM_classes.MultiDialog.water_habit.set()
        await Habits.Water.habit_water(message, state)
    # if message.text == 'Работа с телом':
    #     await FSM_classes.MultiDialog.test_typeperson.set()
    #     await PopTests.Pop_Typeperson.pretest_typeperson(message, state)

