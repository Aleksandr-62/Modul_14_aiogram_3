import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

start_router = Router()
# Запуск бота
async def main():
    bot = Bot(token="???????????????????????????????????????????")
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

start_kb = ReplyKeyboardMarkup(
    keyboard = [
        [
        KeyboardButton(text = "Рассчитать"),
        KeyboardButton(text = "Информация")
        ]
    ], resize_keyboard=True
)

@start_router.message(CommandStart())  # перехватывает команды после "/" в данном случае "/start"
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = start_kb)

@start_router.message(F.text == "Рассчитать") # перехватывает текстовое сообщение
async def start_router_process(message: Message, state: FSMContext):
    await message.answer("Введите свой возраст")
    await state.set_state(UserState.age)

@start_router.message(F.text, UserState.age)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await state.set_state(UserState.growth)

@start_router.message(F.text, UserState.growth)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await state.set_state(UserState.weight)

@start_router.message(F.text, UserState.weight)
async def start_router_process(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    result1 = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'Ваша норма калорий: {result} ккал в сутки (для мужчин)\n'
                         f'Ваша норма калорий: {result1} ккал в сутки (для женщин)')
    await state.clear()

if __name__ == "__main__":
    asyncio.run(main())
