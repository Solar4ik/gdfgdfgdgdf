import asyncio
import io
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction
import keyboards_handers

dp = Dispatcher()
bot = Bot('6497474153:AAEYBrxR66f_KpSVb00__JRuCI8Lp6AuMZ4')
updateskb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='0.2', callback_data='0.2'),
            InlineKeyboardButton(text='0.3', callback_data='0.3'),
        ]
    ]
)

@dp.callback_query(lambda c: c.data.startswith('0.'))
async def process_callback(callback_query: CallbackQuery):
    await callback_query.answer()

    if callback_query.data == '0.2':
        await callback_query.message.answer('[0.2]15.02.24.В данном обновлении мы добавили скачку видео с ютуба в найлучшем качестве которое предоставляет API\nЭто ещё не финал, и мы стремимся к большему. Разработчики в поисках лучшего API который сделает работу с нашим ботом намного приятнее ✅')
    elif callback_query.data == '0.3':
        await callback_query.message.answer('[0.3]16.02.24.В данном обновлении мы поправили взаимодействие с командами, теперь стало намного легче т.к мы добавили кнопки и изменили поведение ответа если ввёл неправильный URL✅')
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, отправь нам ссылку на тикток или YouTube, и я отправлю видео без водяного знака\nДля взаимодействия с командами, выберите нужную команду с кнопок ",reply_markup=keyboards_handers.main_kb)

@dp.message()
async def commands_handler(message: types.Message):
    msg = message.text.lower()
    if msg == 'problems' :
        await message.answer(
            'Список проблем в боте которые мы стремимся исправить:\nБольшое время отзыва у API\nМедленная отправка '
            'файлов\nнету выбора разрешений(проблема с API)\nИногда возникают ошибки в коде во время использовния '
            'бота\nОтсуствие кнопок для удобства в использовании\nНо не стоит забыть что бот ещё сырой,'
            'и это не конечная версия😉')
    if msg == 'updates' :
        await message.answer("Выберите обновление из списка", reply_markup=updateskb) 
    if msg == "func":
        await message.answer('Youtube - ✅\nTikTok - ✅\nReddit - ⛔\nTwitter - ⛔\nFacebook - ⛔\nInstagram- ⛔  ' )
    if msg == "help":
        await message.answer('Для помощи или в случае непредсказуемых ошибок, напишите - @Solarka')
@dp.message()
async def process_message(message: types.Message):
    text = message.html_text
    try:
        if 'https://www.tiktok.com/' in text or 'https://vm.tiktok.com/' in text:
            msg_anw2 = await message.answer('⌛')
            link_tt = text
            url_vid = await fetch_video(link_tt)

            if url_vid:
                await send_file(message, url_vid)
                await bot.delete_message(chat_id=msg_anw2.chat.id, message_id=msg_anw2.message_id)
            else:
                await message.answer('Не удалось загрузить видео с TikTok. Пожалуйста, попробуйте другую ссылку.')

        if 'https://www.youtube.com/' in text or 'https://youtu.be/' in text:
            msg_anw1 = await message.answer('⌛')
            link_yt = text
            url_vid = await fetch_youtube_video(link_yt)

            if url_vid:
                await send_file(message, url_vid)
                await bot.delete_message(chat_id=msg_anw1.chat.id, message_id=msg_anw1.message_id)
            else:
                await message.answer('Не удалось загрузить видео с YouTube. Пожалуйста, попробуйте другую ссылку.')

    except Exception as e:
        print(e)


async def fetch_video(link):
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    querystring = {"url": link, "hd": "1"}

    headers = {
        "X-RapidAPI-Key": "7d5e940360mshd3b8e8e5b90b830p1c279djsn4e035800944e",
        "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                data = await response.json()
                return data['data']['play']
    except Exception as e:
        print(e)


async def fetch_youtube_video(link):
    url = "https://youtube-audio-video-download.p.rapidapi.com/geturl"
    querystring = {"video_url": link}
    headers = {
        "X-RapidAPI-Key": "7d5e940360mshd3b8e8e5b90b830p1c279djsn4e035800944e",
        "X-RapidAPI-Host": "youtube-audio-video-download.p.rapidapi.com"
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=querystring) as response:
                data = await response.json()
                return data.get('video_high')
    except Exception as e:
        print(e)


async def send_file(message: types.Message, url_vid):
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    file = io.BytesIO()
    url = url_vid
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result_bytes = await response.read()

    file.write(result_bytes)
    await message.reply_document(
        document=types.BufferedInputFile(
            file=file.getvalue(),
            filename='video.mp4'
        ),
    )


async def main():
    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
