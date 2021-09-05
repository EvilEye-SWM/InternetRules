import hashlib
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.types import Message, InlineQuery, InputTextMessageContent, InlineQueryResultArticle

rule_dict = {
    '1': 'Не говори о /b/.',
    '2': 'Вообще НИКОГДА не говори о /b/.',
    '3': 'Мы - Анонимус.',
    '4': 'Имя нам - Легион.',
    '5': 'Анонимус не прощает.',
    '6': 'Анонимус может быть ужасным бездушным монстром.',
    '7': 'Анонимус доставляет.',
    '8': 'Правил не существует.',
    '9': 'Для модераторов правил тоже не существует — наслаждайтесь баном.',
    '10': 'Не прелюбодействуй с другими сайтами.',
    '11': 'Любое утверждение должно быть подкреплено пруфлинком.',
    '12': 'Ничего святого нет.',
    '13': 'Не корми тролля.',
    '14': 'Все твои тщательно подобранные аргументы могут быть проигнорированы.',
    '15': 'В интернетах девушек нет.',
    '17': 'TITS or GTFO — выбор за тобой.',
    '19': 'Капитан Очевидность всегда спешит на помощь.',
    '20': 'Любой репост — это репост репоста.',
    '21': 'Этому треду не хватает гомосексуальных негров.',
    '22': '/b/ сегодня фейлит.',
    '24': 'Ты — тролль, лжец и девственник.',
    '25': 'Этому треду не хватает овощей.',
    '26': 'На ноль делить нельзя. Потому что так сказал калькулятор.',
    '27': 'Не следует разговаривать с копипастой. Это глупо.',
    '28': 'CAPSLOCK — ЭТО АВТОПИЛОТ ДЛЯ ВИНА!',
    '29': 'ДАЖЕ С АВТОПИЛОТОМ НУЖНО СООБРАЖАТЬ, КУДА ЕДЕШЬ.',
    '33': 'Один положительный коммент о Японии — и ты вап-кун.',
    '34': 'С этим есть порно. Никаких исключений.',
    '35': 'Если поорна нет, его скоро сделают.',
    '36': 'Фапать и шликать можно на всё.',
    '38': 'С этим есть фурри-порно.',
    '41': 'К любой программе найдётся кряк.',
    '42': 'Исключений для правила 34 не существует. Это касается самого правила 34.',
    '43': 'Интернеты состоят на 95% из школоты.',
    '44': 'Фактов и дефактов нет! Любое мнение в интернетах субъективно, относительно и жутко абстрактно.',
    '45': 'Админ главнее тебя, пади ниц.',
    '46': 'Заканчивать предложения местоимениями/предлогами/междометиями не круто.'
          ' Серьезно, это хуже чем шутки Чака Нориса ',
    '47': 'Какое бы дерьмо вы не увидели, дальше будет еще жестче',
    '48': 'На любой контент есть ♂Right Version♂.',
    '49': 'Правило 44 — ложь.',
    '50': '???????',
    '51': 'ПРОФИТ',
    '52': 'Всегда спрашивай о поле собеседника — на всякий случай, но на самом деле это мужчина. ',
    '53': 'В интернете все девушки — мужчины, а все дети — тайные агенты ФБР.',
    '54': 'Неважно, что это — оно всегда кому-то нравится.',
    '55': 'Чем красивей и чище что-либо — тем больше нас радует его осквернение.'
}


async def start(m: Message):
    await m.answer('Привет!'
                   '\n\nВ этом боте собрана самая большая база правил интернета. '
                   'Для её использования используй /rule'
                   '\nМой исходный код: https://github.com/EvilEye-SWM/InternetRules')


async def rules(m: Message):
    args = m.get_args()
    with suppress(Exception):
        if args == '':
            await m.answer('Для того, чтобы выслать правило укажи его номер. От 1 до 55.')
        elif 1 <= len(args) <= 2:
            if m.reply_to_message is None:
                await m.reply(rule_dict[args])
            else:
                await m.bot.send_message(text=rule_dict[args],
                                         chat_id=m.reply_to_message.chat.id,
                                         reply_to_message_id=m.reply_to_message.message_id)


async def inline(inline_query: InlineQuery):
    text = inline_query.query

    if not text.isdigit():
        title = 'Ошибка'
        description = 'Введите правило числом!'
        input_content = InputTextMessageContent('Введите правило числом!')
    else:
        try:
            title = f'Правило {text}'
            description = rule_dict[text]
            input_content = InputTextMessageContent(rule_dict[text])
        except KeyError:
            title = 'Ошибка'
            description = 'Правило можно указать только от 1 до 55.'
            input_content = InputTextMessageContent('Правило можно указать только от 1 до 55.')

    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(
        id=result_id,
        title=title,
        input_message_content=input_content,
        description=description
    )
    await inline_query.bot.answer_inline_query(inline_query.id, results=[item])


def register_user(dp: Dispatcher):
    dp.register_message_handler(rules, commands=["rule"])
    dp.register_message_handler(start, commands=["start"])
    dp.register_inline_handler(inline)
