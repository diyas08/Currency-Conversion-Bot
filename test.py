import logging
import requests
import time
from aiogram.types import ContentType
from currency_converter import CurrencyConverter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from config import API_TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from keyboards.default.default_buttons import *
from states import UserState

bot = (Bot(token=API_TOKEN))
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

url = "https://nbu.uz/en/exchange-rates/json/"
response = requests.get(url)


@dp.message_handler(commands="start")
async def welcome(message: types.Message):
    await message.answer("""
***Assalomu Aleykum*** 
  """, reply_markup=menu)


@dp.message_handler(text="Kurs")
async def kurs_valut(message: types.Message):
    if response.status_code == 200:
        data = response.json()

        for item in data:
            country = item.get('title', 'N/A')
            code_curr = item.get('code', 'N/A')
            kurs = item.get('cb_price', 'N/A')
            nbu_buy_price = item.get('nbu_buy_price') or "Nomalum"
            nbu_cell_price = item.get('nbu_cell_price') or "Nomalum"
            date = item.get('date', 'N/A')
            await message.answer(f"""
Davlat: {country}
Valuta kodi: {code_curr}
Kurs: {kurs}
Sotib olish narxi (NBU): {nbu_buy_price}
Sotish narxi (NBU): {nbu_cell_price}
Oxirgi narx vahti: {date}
""")
            time.sleep(0.7)
    else:
        await message.answer("Error response:", response.status_code)


@dp.message_handler(text="Currency converte")
async def currency_convert(message: types.Message):
    await message.answer("Qancho Uzbekiston so'mini converte qilmoqchisiz? Sonini yuboring!")
    count = int(message.text)
    if response.status_code == 200:
        data = response.json()

        for item in data:
            country = item.get('title', 'N/A')
            code_curr = item.get('code', 'N/A')
            kurs = item.get('cb_price', 'N/A')
            date = item.get('date', 'N/A')
            result_converte = kurs * count

        await message.answer(f"""
Davlat: {country}
Valuta kodi: {code_curr}
Kurs: {kurs} ({date}, vohtidagi kurs)
Converte result: {result_converte}
""")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
