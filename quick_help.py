from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardRemove
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule as schedule

from aiogram.utils.exceptions import BotBlocked

import Markups
from Token import Token
bot = Bot(Token)
dp = Dispatcher(bot, storage=MemoryStorage())


quick_help_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('🤯 Истерика'),
    KeyboardButton('😢 Грусть'),
    KeyboardButton('😠 Раздражение'),
    KeyboardButton('😔 Упадок сил'),
    KeyboardButton('🙄 Безразличие'),
    KeyboardButton('😩 Отчаяние'),
    KeyboardButton('😧 Страх'))

hysterics0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics0'))
sadness0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness0'))
irritation0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation0'))
prostration0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration0'))
indifference0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference0'))
despair0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair0'))
fear0 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear0'))


async def all_way_quick_help(message:types.Message):
    if message.text == '🤯 Истерика':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=hysterics0)
    elif message.text == '😢 Грусть':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=sadness0)
    elif message.text == '😠 Раздражение':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=irritation0)
    elif message.text == '😔 Упадок сил':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=prostration0)
    elif message.text == '🙄 Безразличие':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=indifference0)
    elif message.text == '😩 Отчаяние':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=despair0)
    elif message.text == '😧 Страх':
        await bot.send_message(message.from_user.id,
                               text='Я знаю, что ты стараешься и уделяешь много внимания клиентам',
                               reply_markup=Markups.backHabitRe)
        await bot.send_message(message.from_user.id,
                               text='Сегодня у тебя трудный день, однако не стоит заполнять себя этими мыслями',
                               reply_markup=fear0)


hysterics1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics1'))
sadness1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness1'))
irritation1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation1'))
prostration1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration1'))
indifference1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference1'))
despair1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair1'))
fear1 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear1'))

hysterics2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics2'))
sadness2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness2'))
irritation2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation2'))
prostration2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration2'))
indifference2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference2'))
despair2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair2'))
fear2 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear2'))

hysterics3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='hysterics3'))
sadness3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='sadness3'))
irritation3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='irritation3'))
prostration3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='prostration3'))
indifference3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='indifference3'))
despair3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='despair3'))
fear3 = InlineKeyboardMarkup().add(InlineKeyboardButton('Приступим', callback_data='fear3'))

hysterics4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='hysterics4'))
sadness4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='sadness4'))
irritation4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='irritation4'))
prostration4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='prostration4'))
indifference4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='indifference4'))
despair4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='despair4'))
fear4 = InlineKeyboardMarkup().add(InlineKeyboardButton('Хорошо! А что делать дальше?', callback_data='fear4'))

hysterics5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='hysterics5'))
sadness5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='sadness5'))
irritation5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='irritation5'))
prostration5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='prostration5'))
indifference5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='indifference5'))
despair5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='despair5'))
fear5 = InlineKeyboardMarkup().add(InlineKeyboardButton('Продолжай', callback_data='fear5'))

hysterics6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='hysterics6'))
sadness6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='sadness6'))
irritation6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='irritation6'))
prostration6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='prostration6'))
indifference6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='indifference6'))
despair6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='despair6'))
fear6 = InlineKeyboardMarkup().add(InlineKeyboardButton('Спасибо! Что ещё мне посоветуешь?', callback_data='fear6'))


async def all_way_callback_quick_help(callback_query: types.CallbackQuery):
    if callback_query.data[:-1] == 'hysterics':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Самое важное сейчас - успокоиться. Глубоко вдохни и постепенно начинай выравнивать своё дыхание',
                                   reply_markup=hysterics1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Я понимаю, что сейчас ситуация накаляется. Давай сфокусируемся на том, что можно сделать, чтобы помочь решить проблему',
                                   reply_markup=hysterics2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=hysterics3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Очень важно, чтобы ты взял небольшую паузу для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугублять свое состояние. '
                                        '\nДля этого предлагаю следующий набор рекомендаций: встань со своего рабочего места и сделай небольшую прогулку, можешь также выпить стакан воды или сделать чашечку горячего чая. '
                                        '\nЭти маленькие паузы помогут отвлечься и успокоиться.',
                                   reply_markup=hysterics4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Теперь давайте выполним разгрузку нервной системы через дыхательную практику:'
                                        '\n\n - Найди удобное место, где ты сможешь сосредоточиться и провести дыхательные практики.'
                                        '\n - Сядь или встань в удобную позицию, удерживая спину прямой.'
                                        '\n - Положи одну руку на живот, а другую на грудь.'
                                        '\n - Закрой глаза или сфокусируйтесь на одной точке перед собой.'
                                        '\n - Начни медленно вдыхать через нос, чувствуя, как воздух наполняет живот, а затем грудь. При этом дыхание должно быть глубоким и расслабленным.'
                                        '\n - Постепенно задержи дыхание на секунду или две.'
                                        '\n - Медленно выдыхай через рот, представляя, что ты выпускаешь напряжение и тревогу из своего тела.'
                                        '\n - Повтори этот цикл глубокого вдоха и выдоха 5-10 раз или до тех пор, пока не почувствуешь себя более спокойным и расслабленным.'
                                        '\n - Если тебе комфортно, можешь продолжить практику дыхания, увеличивая количество циклов или удлиняя время задержки дыхания.'
                                        '\n - Возможно, тебе также поможет выпить немного воды или сделать небольшую прогулку для еще большего расслабления.'
                                        '\n - Помни, что дыхательные практики можно выполнять в любое время, когда ты чувствуешь необходимость в снижении уровня тревоги и напряжения. Их ты можешь найти в разделе "Практики" в главном меню или используя команду /practices',
                                   reply_markup=hysterics5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=hysterics6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)

    elif callback_query.data[:-1] == 'sadness':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Грусть - это нормальное чувство, не нужно это скрывать, ты не одинок. Если нужно, найди место, где ты сможешь отдохнуть и восстановиться',
                                   reply_markup=sadness1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Ты очень отзывчивый человек, и твоя эмпатия помогает клиентам почувствовать себя важными',
                                   reply_markup=sadness2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=sadness3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Очень важно, чтобы ты взял небольшую паузу для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугублять свое состояние. '
                                        '\nДля этого предлагаю следующий набор рекомендаций: встань со своего рабочего места и сделай небольшую прогулку, можешь также выпить стакан воды или сделать чашечку горячего чая. '
                                        '\nЭти маленькие паузы помогут отвлечься и успокоиться.',
                                   reply_markup=sadness4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Теперь давайте выполним разгрузку нервной системы через дыхательную практику:'
                                        '\n\n - Найди удобное место, где ты сможешь сосредоточиться и провести дыхательные практики.'
                                        '\n - Сядь или встань в удобную позицию, удерживая спину прямой.'
                                        '\n - Положи одну руку на живот, а другую на грудь.'
                                        '\n - Закрой глаза или сфокусируйтесь на одной точке перед собой.'
                                        '\n - Начни медленно вдыхать через нос, чувствуя, как воздух наполняет живот, а затем грудь. При этом дыхание должно быть глубоким и расслабленным.'
                                        '\n - Постепенно задержи дыхание на секунду или две.'
                                        '\n - Медленно выдыхай через рот, представляя, что ты выпускаешь напряжение и тревогу из своего тела.'
                                        '\n - Повтори этот цикл глубокого вдоха и выдоха 5-10 раз или до тех пор, пока не почувствуешь себя более спокойным и расслабленным.'
                                        '\n - Если тебе комфортно, можешь продолжить практику дыхания, увеличивая количество циклов или удлиняя время задержки дыхания.'
                                        '\n - Возможно, тебе также поможет выпить немного воды или сделать небольшую прогулку для еще большего расслабления.'
                                        '\n - Помни, что дыхательные практики можно выполнять в любое время, когда ты чувствуешь необходимость в снижении уровня тревоги и напряжения. Их ты можешь найти в разделе "Практики" в главном меню или используя команду /practices',
                                   reply_markup=sadness5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=sadness6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)
    elif callback_query.data[:-1] == 'irritation':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Попробуй найти способ расслабиться, дыши глубоко и делай небольшие паузы. Помни, что клиенты могут испытывать свои трудности, и твоя поддержка им очень важна',
                                   reply_markup=irritation1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text=' Ты важная часть команды, и я готов помочь тебе разобраться с любыми трудностями, с которыми ты сталкиваешься. Можем вместе обсудить пути борьбы с раздражением',
                                   reply_markup=irritation2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=irritation3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Очень важно, чтобы ты взял небольшую паузу для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугублять свое состояние. '
                                        '\nДля этого предлагаю следующий набор рекомендаций: встань со своего рабочего места и сделай небольшую прогулку, можешь также выпить стакан воды или сделать чашечку горячего чая. '
                                        '\nЭти маленькие паузы помогут отвлечься и успокоиться.',
                                   reply_markup=irritation4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Теперь давайте выполним разгрузку нервной системы через дыхательную практику:'
                                        '\n\n - Найди удобное место, где ты сможешь сосредоточиться и провести дыхательные практики.'
                                        '\n - Сядь или встань в удобную позицию, удерживая спину прямой.'
                                        '\n - Положи одну руку на живот, а другую на грудь.'
                                        '\n - Закрой глаза или сфокусируйтесь на одной точке перед собой.'
                                        '\n - Начни медленно вдыхать через нос, чувствуя, как воздух наполняет живот, а затем грудь. При этом дыхание должно быть глубоким и расслабленным.'
                                        '\n - Постепенно задержи дыхание на секунду или две.'
                                        '\n - Медленно выдыхай через рот, представляя, что ты выпускаешь напряжение и тревогу из своего тела.'
                                        '\n - Повтори этот цикл глубокого вдоха и выдоха 5-10 раз или до тех пор, пока не почувствуешь себя более спокойным и расслабленным.'
                                        '\n - Если тебе комфортно, можешь продолжить практику дыхания, увеличивая количество циклов или удлиняя время задержки дыхания.'
                                        '\n - Возможно, тебе также поможет выпить немного воды или сделать небольшую прогулку для еще большего расслабления.'
                                        '\n - Помни, что дыхательные практики можно выполнять в любое время, когда ты чувствуешь необходимость в снижении уровня тревоги и напряжения. Их ты можешь найти в разделе "Практики" в главном меню или используя команду /practices',
                                   reply_markup=irritation5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=irritation6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)
    elif callback_query.data[:-1] == 'prostration':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Ты уже проделал много работы и справился со многими вызовами. Позволь себе небольшую паузу, чтобы отдохнуть и восстановить энергию. Помни, что ты ценен и твоя работа имеет значение',
                                   reply_markup=prostration1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знаю, что иногда бывает сложно поддерживать позитивный настрой, но не забывай, что важно заботиться о своем благополучии. Если ты не против, я помогу тебе найти способы восстановления энергии и поддержания баланса в течение дня',
                                   reply_markup=prostration2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=prostration3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Советуем тебе придерживаться постоянного режима сна. '
                                        '\nПостарайся ложиться и вставать в одно и то же время каждый день, даже в выходные. '
                                        'Это поможет синхронизировать ритмы организма и способствовать улучшению качества сна. '
                                        '\nТы можешь настроить свой режим сна в разделе "Привычки" в главном меню.',
                                   reply_markup=prostration4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Несколько советов по улучшению качества сна:'
                                        '\n - Создание комфортной среды для сна. Это включает тихую и прохладную комнату, удобную кровать, подходящую подушку и постельное белье. Также помните о важности темноты и отсутствии сильного освещения, а также о затишье и тишине.'
                                        '\n - Избегание стимулирующих веществ, таких как кофеин, никотин и алкоголь перед сном. Эти вещества могут негативно влиять на качество сна и вызывать беспокойство или бессонницу.'
                                        '\n - Расслабляющие ритуалы перед сном помогают расслабиться и готовиться ко сну. Это может быть теплая ванна, чтение книги, медитация или расслабляющая музыка. Важно выбрать то, что работает лучше всего для вас, это подбирается опытным путем.'
                                        '\n - Синий свет, который излучают экранные устройства, негативно сказываются на качество сна. Рекомендуем ограничивать использование смартфонов, планшетов и компьютеров перед сном. Лучше заменить экранные активности на более расслабляющие занятия.'
                                        '\n - Помни, что стресс может негативно влиять на качество сна. Поэтому стоит задуматься о том, что возможно проблема упадка сил вовсе не связана с качеством сна.',
                                   reply_markup=prostration5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=prostration6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)
    elif callback_query.data[:-1] == 'indifference':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Если тебе кажется, что потерял интерес или мотивацию, попробуй вспомнить, какое влияние ты оказываешь на клиентов и их проблемы. Необходимо придать своей работе новый смысл и постараться найти в ней радость и удовлетворение',
                                   reply_markup=indifference1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Сейчас тебе может казаться, что каждый звонок одинаковый. Но помни, что твоя работа имеет значение для каждого клиента, которому ты помогаешь. Давай найдем способы, чтобы каждый звонок был для тебя интересным, а значимость твоей работы была наглядна видна',
                                   reply_markup=indifference2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=indifference3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Такая реакция направлена на защиту психики человека. Если ты чувствуешь упадок сил, если тебе трудно собраться и начать что-то делать, и особенно, если ты понимаешь, что не способен испытывать эмоции, то это точно апатия.'
                                        '\nОчень важно, чтобы ты взял небольшую паузу прямо сейчас для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугубить свое состояние.',
                                   reply_markup=indifference4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Давай рассмотрим самые простые и эффективные приёмы самопомощи, которые помогут тебе избавиться от плохого самочувствия:'
                                        '\n 1) Дай себе возможность отдохнуть при первой же возможности;'
                                        '\n 2) Сними обувь, прими удобную позу, постарайся расслабиться;'
                                        '\n 3) Не злоупотребляй напитками, содержащими кофеин (кофе, крепкий чай);'
                                        '\n 4) Помести в тепло ноги, следи за тем, чтобы твое тело не было напряжено;'
                                        '\n 5) Если ситуация требует от тебя действий, дай себе короткий отдых, расслабься, хотя бы 15-20 минут;'
                                        '\n 6) Помассируй мочки ушей и пальцы рук - это места, где находится огромное количество биологически активных точек;'
                                        '\n 7) Выпей чашку некрепкого сладкого чая;'
                                        '\n 8) Сделай несколько физических упражнений, но не в быстром темпе;'
                                        '\n 9) После этого приступай к выполнению тех дел, которые необхо­димо сделать;'
                                        '\n 10) Выполняй работу в среднем темпе, старайся сохранять силы;'
                                        '\n 11) Не берись делать несколько дел сразу, в таком состоянии внимание рассеяно, и сконцентрироваться, а особенно на нескольких делах трудно.',
                                   reply_markup=indifference5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=indifference6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)
    elif callback_query.data[:-1] == 'despair':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Время от времени мы можем чувствовать отчаяние, особенно когда сталкиваемся с трудностями. Помни, что даже в трудных ситуациях есть решения',
                                   reply_markup=despair1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знай, я здесь, чтобы поддержать тебя, и вместе найти способы преодолеть трудные моменты. Помни, что ты не один и всегда можешь обратиться за поддержкой!',
                                   reply_markup=despair2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=despair3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Очень важно, чтобы ты взял небольшую паузу для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугублять свое состояние. '
                                        '\nДля этого предлагаю следующий набор рекомендаций: встань со своего рабочего места и сделай небольшую прогулку, можешь также выпить стакан воды или сделать чашечку горячего чая. '
                                        '\nЭти маленькие паузы помогут отвлечься и успокоиться.',
                                   reply_markup=despair4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Несколько рекомендаций для того, чтобы помочь справиться с состоянием:'
                                        '\n 1. Глубоко дыши. Это прекрасная возможность снять стресс — быстро, эффективно и незаметно даже в многолюдном офисе. Просто вдохни на четыре счета, а затем так же на четыре счета выдохни.'
                                        '\n 2. Давай своему организму физическую нагрузку. Регулярные занятия спортом улучшают настроение, повышают уверенность в себе и помогают расслабиться. Эти преимущества помогают снизить общий уровень стресса и дать ощущение контроля над своим телом и своей жизнью.'
                                        '\n 3. Делай перерывы. Достаточно делать 10-15 минутные перерывы в течение рабочего дня - походить, сделать небольшую разминку, потянуться, выйти на свежий воздух. Также, постарайся менять положение твоего тела при работе.'
                                        '\n 4. Установи личные границы при работе с клиентами. При возникновении конфликтных и затруднительных ситуаций с клиентами отстраняйсся от ситуации, напоминая себе, что клиент не предъявляет претензии лично к тебе, он делает это в отношении компании, в которой ты работаешь. Не воспринимая отношение клиентов лично, ты спасешь себя от эмоциональных перегрузок и снижения чувства вины.'
                                        '\n 5. Пообщайся с коллегами. Сталкиваясь со сложностями, важно найти тех людей, которые испытывают аналогичные проблемы. Поэтому, крайне необходимо при возникновении затруднительных, волнующих тебя обстоятельств, обсуждать мысли и эмоции с теми людьми, которые смогут тебя понять и поделятся своим опытом и способами преодоления сложных ситуаций.'
                                        '\n 6. Обращайся за помощью. В ситуациях, когда ты не понимаешь, как учше поступить, ты не обладаешь достаточным количеством информации или компетенций, не стесняйся задавать вопросы коллегам и наставникам. Не стоит пытаться решить проблему исключительно собственными силами, ведь есть вероятность, что ты потратишь на это гораздо больше сил и времени, чем мог бы потратить, обратившись за помощью.'
                                        '\n 7. Вспоминай о том, что для тебя важно. Использование журналов благодарностей повышает внимание, восприимчивость и энергичность, а также способствует укреплению иммунной системы и снижению тревожности.'
                                        '\n 8. Создай на рабочем месте благоприятную обстановку. Обустрой своё рабочее место таким образом, чтобы оно тебя радовало. Эти небольшие вещи сделают рабочий процесс приятнее, и твое внутреннее состояние спокойнее.',
                                   reply_markup=despair5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=despair6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)
    elif callback_query.data[:-1] == 'fear':
        if callback_query.data[-1] == '0':
            await bot.send_message(callback_query.from_user.id,
                                   text='Страх может быть естественной реакцией на сложные ситуации. Постепенно преодолевай свои страхи, шаг за шагом',
                                   reply_markup=fear1)
        elif callback_query.data[-1] == '1':
            await bot.send_message(callback_query.from_user.id,
                                   text='Знай, я здесь, чтобы поддержать тебя, и вместе найти способы преодолеть трудные моменты. Помни, что ты не один и всегда можешь обратиться за поддержкой!',
                                   reply_markup=fear2)
        elif callback_query.data[-1] == '2':
            await bot.send_message(callback_query.from_user.id,
                                   text='Тебе сейчас не легко, но мы постараемся поработать с твоим состоянием чтобы тебе стало полегче. \nДальше мы разберём список шагов, которые помогут эмоционально разгрузиться и избавиться от негативных эмоций',
                                   reply_markup=fear3)
        elif callback_query.data[-1] == '3':
            await bot.send_message(callback_query.from_user.id,
                                   text='Очень важно, чтобы ты взял небольшую паузу для того, чтобы отвлечься от ситуации. Самое важное сейчас - не усугублять свое состояние. '
                                        '\nДля этого предлагаю следующий набор рекомендаций: встань со своего рабочего места и сделай небольшую прогулку, можешь также выпить стакан воды или сделать чашечку горячего чая. '
                                        '\nЭти маленькие паузы помогут отвлечься и успокоиться.',
                                   reply_markup=fear4)
        elif callback_query.data[-1] == '4':
            await bot.send_message(callback_query.from_user.id,
                                   text='Несколько рекомендаций для того, чтобы помочь справиться с состоянием:'
                                        '\n 1. Глубоко дыши. Это прекрасная возможность снять стресс — быстро, эффективно и незаметно даже в многолюдном офисе. Просто вдохни на четыре счета, а затем так же на четыре счета выдохни.'
                                        '\n 2. Давай своему организму физическую нагрузку. Регулярные занятия спортом улучшают настроение, повышают уверенность в себе и помогают расслабиться. Эти преимущества помогают снизить общий уровень стресса и дать ощущение контроля над своим телом и своей жизнью.'
                                        '\n 3. Делай перерывы. Достаточно делать 10-15 минутные перерывы в течение рабочего дня - походить, сделать небольшую разминку, потянуться, выйти на свежий воздух. Также, постарайся менять положение твоего тела при работе.'
                                        '\n 4. Установи личные границы при работе с клиентами. При возникновении конфликтных и затруднительных ситуаций с клиентами отстраняйсся от ситуации, напоминая себе, что клиент не предъявляет претензии лично к тебе, он делает это в отношении компании, в которой ты работаешь. Не воспринимая отношение клиентов лично, ты спасешь себя от эмоциональных перегрузок и снижения чувства вины.'
                                        '\n 5. Пообщайся с коллегами. Сталкиваясь со сложностями, важно найти тех людей, которые испытывают аналогичные проблемы. Поэтому, крайне необходимо при возникновении затруднительных, волнующих тебя обстоятельств, обсуждать мысли и эмоции с теми людьми, которые смогут тебя понять и поделятся своим опытом и способами преодоления сложных ситуаций.'
                                        '\n 6. Обращайся за помощью. В ситуациях, когда ты не понимаешь, как учше поступить, ты не обладаешь достаточным количеством информации или компетенций, не стесняйся задавать вопросы коллегам и наставникам. Не стоит пытаться решить проблему исключительно собственными силами, ведь есть вероятность, что ты потратишь на это гораздо больше сил и времени, чем мог бы потратить, обратившись за помощью.'
                                        '\n 7. Вспоминай о том, что для тебя важно. Использование журналов благодарностей повышает внимание, восприимчивость и энергичность, а также способствует укреплению иммунной системы и снижению тревожности.'
                                        '\n 8. Создай на рабочем месте благоприятную обстановку. Обустрой своё рабочее место таким образом, чтобы оно тебя радовало. Эти небольшие вещи сделают рабочий процесс приятнее, и твое внутреннее состояние спокойнее.',
                                   reply_markup=fear5)
        elif callback_query.data[-1] == '5':
            await bot.send_message(callback_query.from_user.id,
                                   text='Подумай о позитивных моментах: вспомни хорошие моменты или успехи, которые ты достиг в работе или в жизни. '
                                        '\nФокусирование на положительных аспектах может помочь изменить настроение.'
                                        '\nПоддерживай свою эмоциональную и физическую форму: удели время для заботы о себе, убедись, что ты получаешь достаточно сна, правильно питаешься и регулярно занимаешься физическими упражнениями',
                                   reply_markup=fear6)
        elif callback_query.data[-1] == '6':
            await bot.send_message(callback_query.from_user.id,
                                   text='Важно помнить, что негативные эмоции - это естественная реакция на стресс. Для улучшения самоконтроля выполняй практики и следуй набору рекомендаций от бота.'
                                        '\nРегулярное выполнение психологических практик позволит снять эмоциональное напряжение и разгрузить нервную систему.'
                                        '\n\nЕсли негативные эмоции возникают у тебя всё чаще и чаще, мешают твоей повседневной жизни и работе, то мы рекомендуем тебе обратиться к профессиональному психологу для получения дополнительной поддержки и советов.',
                                   reply_markup=Markups.backHabitRe)


def register_handlers_quick_help(dp: Dispatcher):
    dp.register_callback_query_handler(
        all_way_callback_quick_help, text=['hysterics0', 'sadness0', 'irritation0', 'prostration0', 'indifference0', 'despair0', 'fear0',
                                           'hysterics1', 'sadness1', 'irritation1', 'prostration1', 'indifference1', 'despair1', 'fear1',
                                           'hysterics2', 'sadness2', 'irritation2', 'prostration2', 'indifference2', 'despair2', 'fear2',
                                           'hysterics3', 'sadness3', 'irritation3', 'prostration3', 'indifference3', 'despair3', 'fear3',
                                           'hysterics4', 'sadness4', 'irritation4', 'prostration4', 'indifference4', 'despair4', 'fear4',
                                           'hysterics5', 'sadness5', 'irritation5', 'prostration5', 'indifference5', 'despair5', 'fear5',
                                           'hysterics6', 'sadness6', 'irritation6', 'prostration6', 'indifference6', 'despair6', 'fear6'])

