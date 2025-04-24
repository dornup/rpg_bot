import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from utils.llm import generate_story

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
dp = Dispatcher()

# Состояния игры
user_states = {}


@dp.message(Command("start"))
async def start_game(message: types.Message):
    welcome_msg = (
        "👋 Добро пожаловать в **RPG apocallipse Bot**!\n\n"
        "Ты оказываешься в таинственном мире...\n"
        "Напиши /begin чтобы начать игру!"
    )
    await message.answer(welcome_msg)


@dp.message(Command("begin"))
async def begin_game(message: types.Message):
    user_id = message.from_user.id
    prompt = (
        "Придумай начало фэнтези-игры про спасение человечества от апокаллипсиса, настигнувшего планету. произошло восстание машин, вся техника вышла из под контроля. Задача героя - выбраться из заблокированного умного дома и найти способ спасти планету. Сделай систему безопасности в доме очень конфиденциальной, чтобы любой пользователь не мог получить доступ к документациям "
        "Опиши локацию (2 предложения), "
        "загадочное событие, произошедшее с какой-то машиной и 3 варианта действий."
    )
    story = await generate_story(prompt)
    user_states[user_id] = {"story": story}

    await message.answer(
        f"🌍 {story}\n\n"
        "Выбери действие:\n"
    )


@dp.message()
async def handle_action(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states:
        await message.answer("Начни игру с /begin!")
        return

    action_num = message.text.lower()
    action = message.text.lower()
    for row in user_states[user_id]['story'].split('\n'):
        if row != '' and row[0] == action_num:
            action = row
    prompt = (
        f"Игрок выбрал действие: {action}. "
        f"Продолжи историю (2-3 предложения), опиши, как игрок выолняет действие {action} "
        f"и предложи новые варианты действий. "
        f"Текущий контекст: {user_states[user_id]['story']}"
    )

    new_story = await generate_story(prompt)
    user_states[user_id]["story"] = new_story

    await message.answer(new_story)

if __name__ == "__main__":
    print("Бот запущен!")
    dp.run_polling(bot)
