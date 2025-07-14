import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb


from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.Parsing import parsing
from config import client


class ChannelStates(StatesGroup):
    name_written = State()
    period_written = State()
    count_written = State()

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Используй команду /parse")

@router.message(Command('parse'))
async def parce_handler(message: Message, state: FSMContext):
    await message.answer("Дай ссылку на канал: ")
    await state.set_state(ChannelStates.name_written)

@router.message(ChannelStates.name_written)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Способ задания лимита: ", reply_markup=kb.limit)

#------------------------TIME------------------------------------------------------
@router.callback_query(F.data == "time")
async def time_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Укажите длинну периода в...", show_alert=True)
    await callback.message.edit_text(f"Кол-во... ", reply_markup=kb.period)

@router.callback_query(F.data == "years")
async def years_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelStates.period_written)
    await state.update_data(type="years")
    await callback.answer("Вы выбрали года", show_alert=True)
    try:
        await callback.message.edit_text("Введите число лет: ")
    except Exception as e:
        print(f"Ошибка при редактировании текста: {e}")

@router.callback_query(F.data == "months")
async def months_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelStates.period_written)
    await state.update_data(type="months")
    await callback.answer("Вы выбрали месяцы", show_alert=True)
    try:
        await callback.message.edit_text("Введите число месяцев: ")
    except Exception as e:
        print(f"Ошибка при редактировании текста: {e}")

@router.callback_query(F.data == "days")
async def days_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelStates.period_written)
    await state.update_data(type="days")
    await callback.answer("Вы выбрали дни", show_alert=True)
    try:
        await callback.message.edit_text("Введите число дней: ")
    except Exception as e:
        print(f"Ошибка при редактировании текста: {e}")

@router.message(ChannelStates.period_written)
async def period_handler(message: Message, state: FSMContext):
    await state.update_data(period=message.text)
    data = await state.get_data()

    n_days_ago = datetime.now().date()
    if data["type"] == "years":
        n_days_ago -= relativedelta(years=int(data['period']))
    elif data["type"] == "months":
        n_days_ago -= relativedelta(months=int(data['period']))
    else:
        n_days_ago -= relativedelta(days=int(data['period']))
    await message.answer(f'Считать с канала {data['name']} сообщения, начиная с {n_days_ago}?', disable_web_page_preview=True,  reply_markup=kb.yes_no)
    await state.clear()
    await state.update_data(url = data['name'], type="time", offset_date=n_days_ago.strftime("%Y-%m-%d"))


#------------------------TIME------------------------------------------------------

#------------------------COUNT------------------------------------------------------

@router.callback_query(F.data == "count")
async def days_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChannelStates.count_written)
    await callback.message.edit_text("Введите кол-во сообщений: ")

@router.message(ChannelStates.count_written)
async def period_handler(message: Message, state: FSMContext):
    await state.update_data(count=message.text)
    data = await state.get_data()
    await message.answer(f'Считать с канала {data['name']} {data["count"]} сообщений?', disable_web_page_preview=True, reply_markup=kb.yes_no)
    await state.clear()
    await state.update_data(url=data['name'], type="count", limit=data["count"])

#------------------------COUNT------------------------------------------------------


@router.callback_query(F.data == "yes")
async def days_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.basicConfig(level=logging.INFO)
    await callback.message.answer(f"Let's go parsing...")
    async with client:
        entity = await client.get_entity(data['url'])

        if entity is not None:
            channel_name = entity.username

            await parsing(  # ✅ просто await
                channel_name,
                offset_date=(datetime.strptime(data['offset_date'], "%Y-%m-%d").date() if data['type'] == "time" else None),
                limit=(int(data['limit']) if data['type'] == "count" else None)
            )

    await callback.message.answer(f"All done")
    await state.clear()

@router.callback_query(F.data == "no")
async def days_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Если хотите дать новый запрос используйте /parse")

