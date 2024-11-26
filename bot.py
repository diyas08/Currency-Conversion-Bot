import requests
import logging
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import API_TOKEN
from keyboards.default.default_buttons import *
from aiogram.dispatcher import FSMContext
from states import ConvertState
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
url = "https://nbu.uz/en/exchange-rates/json/"
response = requests.get(url)

@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    await message.answer("""
***Assalomu Aleykum!*** 
Valyuta kurslarini ko'rish yoki konvertatsiya qilish uchun menyudan foydalaning.
    """, reply_markup=menu)


@dp.message_handler(text="Kurs")
async def kurs_valut(message: types.Message):
    if response.status_code == 200:
        data = response.json()
        info = ""
        for item in data:
            country = item.get('title', 'N/A')
            code_curr = item.get('code', 'N/A')
            kurs = item.get('cb_price', 'N/A')
            nbu_buy_price = item.get('nbu_buy_price') or "Nomalum"
            nbu_cell_price = item.get('nbu_cell_price') or "Nomalum"
            date = item.get('date', 'N/A')
            info += (f"""
Davlat: {country}
Valyuta kodi: {code_curr}
Kurs: {kurs}
Sotib olish narxi (NBU): {nbu_buy_price}
Sotish narxi (NBU): {nbu_cell_price}
Oxirgi narx vahti: {date}
""")
        await message.answer(info)

    else:
        await message.answer(f"Error response: {response.status_code}")


@dp.message_handler(text="Currency converte")
async def currency_convert(message: types.Message):
    await message.answer("Qancha O'zbekiston so'mini konvertatsiya qilmoqchisiz? Sonini yuboring!")
    await ConvertState.waiting_for_amount.set()


@dp.message_handler(state=ConvertState.waiting_for_amount)
async def process_conversion(message: types.Message, state: FSMContext):
    try:
        user_input = message.text.replace(" ", "")
        amount = int(user_input)
        print(f"Полученная сумма: {amount}")

        if response.status_code == 200:
            data = response.json()
            result = ""

            for item in data:
                country = item.get('title', 'N/A')
                code_curr = item.get('code', 'N/A')
                kurs = item.get('cb_price')
                if kurs and kurs.replace('.', '', 1).isdigit():
                    kurs = float(kurs)
                    converted = round(amount / kurs, 2)
                    result += f"""
Davlat: {country}
Valyuta kodi: {code_curr}
Kurs: {kurs}
Konvertatsiya qilingan miqdor: {converted}
"""

            await message.answer(result)
        else:
            await message.answer(f"Error response: {response.status_code}")

    except ValueError:
        await message.answer("Iltimos, son kiriting!\n/start bosvoring")

    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

