from Database import db_start, data_profile, pre_points_test_motivation, points_test_motivation
import asyncio
import sqlite3
import Markups
import FSM_classes
from json import dumps
from json import loads
from json import load
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.types import Message

questions = load(open("PopTests/questions_motivation.json", "r", encoding="utf-8"))

from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = sqlite3.connect('Databases/Result_Tests/POP_Motivation.db')


def compose_markup(question: int):
    km = InlineKeyboardMarkup(row_width=3)
    for i in range(len(questions[question]["variants"])):
        cd = {
            "question": question,
            "answer": i
        }
        km.insert(InlineKeyboardButton(questions[question]["variants"][i], callback_data=dumps(cd)))
    return km

def reset(uid: int):
    db.set_in_process(uid, False)
    db.change_count(uid, 0)
    db.change_questions_message(uid, 0)
    db.change_current_question(uid, 0)

async def pretest_motivation(message: types.message, state: FSMContext):
    await pre_points_test_motivation(user_id=message.from_user.id, username=message.from_user.username)
    async with state.proxy() as data:
        data['count'] = 0
    async with state.proxy() as data:
        data['points'] = 0
    await points_test_motivation(state, user_id=message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, 'Тест на мотивацию к успеху Т. Элерса'
                           , reply_markup=types.ReplyKeyboardRemove())
    await asyncio.sleep(2)
    await bot.send_message(message.from_user.id, text=questions[0]["text"], reply_markup=compose_markup(0))

@dp.callback_query_handler(lambda c: True)
async def answer_handler(callback: CallbackQuery):
    data = loads(callback.data)
    q = data["question"]
    cur_motivation = db.cursor()

    count = db.get_count(callback.from_user.id)
    if data["answer"] == 0:
        db.change_count(callback.from_user.id, count)
    if data["answer"] == 1:
        db.change_count(callback.from_user.id, count)
    if db.getcount(callback.from_user.id) == len(questions):
        reset(callback.from_user.id)
        await bot.delete_message(callback.from_user.id, msg)
        await bot.send_message(
            callback.from_user.id,
            f" Вы прошли тест\\!\n\n Ваш результат: \\: *{int(cur_motivation.execute('SELECT count FROM points WHERE user_id = ?', (callback.from_user.id)).fetchone()[0])} баллов \\.\n\n *Пройти тест заново* \\- /starttest", parse_mode="MarkdownV2"
        )
        return
    db.commit()
    await bot.edit_message_text(
        questions[q + 1]["text"],
        callback.from_user.id,
        msg,
        reply_markup=compose_markup(q + 1),
        parse_mode="MarkdownV2"
    )


@dp.message_handler(commands=["starttest"])
async def go_handler(message: Message):
    if not db.is_exists(message.from_user.id):
        db.add(message.from_user.id)
    if db.is_in_process(message.from_user.id):
        await bot.send_message(message.from_user.id, "Вы не можете начать тест, потому что вы уже его проходите\\.", parse_mode="MarkdownV2")
        return
    db.set_in_process(message.from_user.id, True)
    msg = await bot.send_message(
        message.from_user.id,
        questions[0]["text"],
        reply_markup=compose_markup(0),
        parse_mode="MarkdownV2"
    )
    db.change_questions_message(message.from_user.id, msg.message_id)
    db.change_current_question(message.from_user.id, 0)
    db.change_count(message.from_user.id, 0)


@dp.message_handler(commands=["finish"])
async def quit_handler(message: Message):
    if not db.is_in_process(message.from_user.id):
        await bot.send_message(message.from_user.id, "Вы ещё не начали тест\\.", parse_mode="MarkdownV2")
        return
    reset(message.from_user.id)
    await bot.send_message(message.from_user.id, "Вы успешно закончили тест\\.", parse_mode="MarkdownV2")


@dp.message_handler(commands=["start"])
async def start(message: Message):
    await message.answer("Методика диагностики личности на мотивацию к успеху Т\\. Элерса. Стимульный материал представляет собой 41 утверждение, на которые испытуемому необходимо дать один из 2 вариантов ответов «да» или «нет». Тест относится к моношкальным методикам. Степень выраженности мотивации к успеху оценивается количеством баллов, совпадающих с ключом.\\.\n\n *Начать тест* \\- /starttest\n*Завершить тест* \\- /finish\n*Помощь* \\- /help", parse_mode="MarkdownV2")


@dp.message_handler(commands=['help'])
async def cmd_answer(message: Message):
    await message.answer("<b> Если возникли проблемы, напишите</b> \n <a href='https://t.me/reformBotHelp'>@reformBotHelp</a><b>.</b>", disable_web_page_preview=True, parse_mode="HTML")