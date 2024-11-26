from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Kurs")
        ],
        [
            KeyboardButton("Currency converte")
        ]
    ], resize_keyboard=True
)