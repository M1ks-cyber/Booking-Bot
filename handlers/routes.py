from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from forms import BookingStates
import os
from dotenv import load_dotenv
from database.requests import add_booking, get_user_bookings



load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")



router = Router()


@router.message(Command("start"))
async def start_command(message: Message):
    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✏️ Записаться")],
            [KeyboardButton(text="📖 Мои записи")]
        ],
        resize_keyboard=True
    )

    await message.answer("👋Добро пожаловать в нашего бота по записям на услуги.\n" \
                        "Выберите действие:", reply_markup=reply_kb)




@router.message(F.text == "✏️ Записаться")
async def booking(message: Message):
    inl_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Стрижка", callback_data="haircut")],
            [InlineKeyboardButton(text="Консультация", callback_data="consultation")],
            [InlineKeyboardButton(text="Маникюр", callback_data="manicure")]
        ]
    )

    await message.answer("Выберите куда хотите записаться:\n\n", reply_markup=inl_keyboard)




@router.callback_query(F.data.in_({"haircut", "consultation", "manicure"}))
async def booking_chosen(callback: CallbackQuery, state: FSMContext):
    service = callback.data

    names = {
        "haircut": "Стрижка",
        "consultation": "Консультация",
        "manicure": "Маникюр",
    }

    await state.update_data(service=names[service])
    await state.set_state(BookingStates.name)

    await callback.message.edit_text(f"Вы выбрали: {names[service]}")
    await callback.message.answer(
    "Теперь введите ваше имя:",
    reply_markup=ReplyKeyboardRemove()
    )   
    
    await callback.answer()



@router.message(BookingStates.name)
async def name_info(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingStates.phone)
    await message.answer("Теперь чтобы с вами связаться нам нужен ваш номер телефона:")



@router.message(BookingStates.phone)
async def phone_info(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    if message.from_user.username:
        username = "@" + message.from_user.username
    else:
        username = "❌"
    await bot.send_message(ADMIN_ID, f"🔔 Новая запись!\n\n"\
                           f"🧑‍💼Услуга: {data['service']}\n"\
                           f"👤Имя: {data['name']}\n"\
                            f"📞Телефон: {data['phone']}\n"\
                            f"🌀Username: {username}\n"\
                            f"🆔ID Пользователя: {message.from_user.id}")



    await add_booking(
        user_id=message.from_user.id,
        service=data["service"],
        name=data["name"],
        phone=data["phone"],
        username=message.from_user.username
    )


    reply_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✏️ Записаться")],
                [KeyboardButton(text="📖 Мои записи")]
            ],
            resize_keyboard=True
        )

    await message.answer("✅ Запрос успешно отпрвлен.\nС вами свяжуться в ближайшее время.", reply_markup=reply_kb)
    await state.clear()



@router.message(F.text == "📖 Мои записи")
async def get_booking_of_user(message: Message):
    bookings = await get_user_bookings(message.from_user.id)

    if not bookings:
        await message.answer("Пока что у вас нет записей.")
        return
    else:
        text = "Ваши записи:\n\n"
        for b in bookings:
            text += (
            f"Услуга: {b.service}\n"
            f"Имя: {b.name}\n"
            f"Телефон: {b.phone}\n"
            f"Дата записи: {b.created_at.strftime("%d.%m.%Y %H:%M")}\n"
            f"-------------------\n"
        )
        await message.answer(text)





    