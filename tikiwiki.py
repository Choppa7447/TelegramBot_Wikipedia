import wikipedia
import re
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = 'ТОКЕН БОТА'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Салют! Отправьте мне любое слово, и я найду его значение на Wikipedia.")

@dp.message_handler()
async def any_text_message(message: types.Message):
    await message.answer(getwiki(message.text))

def getwiki(text):
    try:
        wikipedia.set_lang("ru") # делаем язык вики русский
        ny = wikipedia.page(text)
        wikitext = ny.content[:1000] # ограничение по длинне сообщения
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'Ничего не понятно, но очень интересно! Сформулируйте иначе.'

if __name__ == "__main__":
    executor.start_polling(dp)