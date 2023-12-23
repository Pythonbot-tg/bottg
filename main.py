import requests
from aiogram import Bot, Dispatcher, executor, types

bot = Bot('6328853075:AAGFBCQOif6nkJBEbP49R35jSsW3Xd1uzCw')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'{message.from_user.first_name}, Ты пидор')


@dp.message_handler(commands=['download'])
async def start(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на видео из Instagram, чтобы я скачал его.")


@dp.message_handler()
async def download_video(message: types.Message):
    video_url = message.text
    if 'instagram.com' not in video_url:
        await message.reply("Пожалуйста, отправьте ссылку на видео из Instagram.")
        return

    try:
        response = requests.get(video_url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        if 'video' not in content_type:
            await message.reply("Ссылка не ведет к видео.")
            return

        video_data = response.content
        video_filename = 'video.mp4'
        with open(video_filename, 'wb') as video_file:
            video_file.write(video_data)

        with open(video_filename, 'rb') as video_file:
            await message.reply_video(video_file)

        os.remove(video_filename)

    except requests.exceptions.HTTPError:
        await message.reply("Не удалось загрузить видео. Пожалуйста, проверьте ссылку и попробуйте снова.")

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю.')


if __name__ != '__main__':
    pass
else:
    executor.start_polling(dp)