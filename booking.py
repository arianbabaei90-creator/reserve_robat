import re
from datetime import datetime
import jdatetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import database
import keyboard
from status import AppointmentState

router = Router()


@router.message(F.text == "📅 رزرو نوبت")
async def reserv_handler(message: Message):
    await message.answer(
        "یکی از خدمات زیر را انتخاب کنید",
        reply_markup=keyboard.service()
    )


@router.callback_query(F.data.startswith("service:"))
async def service_handler(callback: CallbackQuery, state: FSMContext):
    service = callback.data.split(":")[1]
    await state.update_data(service=service)
    await state.set_state(AppointmentState.name)
    await callback.message.answer("لطفا نام خود را وارد کنید:")
    await callback.answer()


@router.message(AppointmentState.name)
async def name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await state.set_state(AppointmentState.phone)
    await message.answer("لطفا شماره موبایل خود را وارد کنید")


@router.message(AppointmentState.phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip() if message.text else ""
    phone = phone.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    phone = phone.replace(" ", "").replace("-", "")

    if phone.startswith("+98"):
        phone = "0" + phone[3:]
    elif phone.startswith("0098"):
        phone = "0" + phone[4:]
    elif phone.startswith("98") and len(phone) == 12:
        phone = "0" + phone[2:]

    if not re.fullmatch(r"09\d{9}", phone):
        await message.answer(
            "❌ شماره موبایل نامعتبر است.\n"
            "شماره باید ۱۱ رقم و با 09 شروع شود.\n"
            "مثال: 09123456789"
        )
        return

    await state.update_data(phone=phone)
    await state.set_state(AppointmentState.date)
    await message.answer("لطفا تاریخ خود را انتخاب کنید", reply_markup=keyboard.date())


@router.callback_query(F.data.startswith("data:"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    date = callback.data.split(":", 1)[1]
    await state.update_data(date=date)
    await state.set_state(AppointmentState.time)
    await callback.message.answer(
        "ساعت مورد نظر خود را وارد کنید",
        reply_markup=keyboard.time()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("time:"))
async def select_time(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split(":", 1)[1]
    data = await state.get_data()

    date = data.get("date")
    service = data.get("service")
    name = data.get("name")
    phone = data.get("phone")
    user_id = callback.from_user.id

    if not await database.is_time_available(date, time):
        await callback.answer("این ساعت قبلا رزرو شده است", show_alert=True)
        return

    await state.update_data(time=time)
    await database.add_user(user_id, name, phone)

    created_at = datetime.now().isoformat()
    await database.add_appointment(user_id, service, date, time, "active", created_at)

    try:
        d = jdatetime.date.fromisoformat(date)
        readable_date = d.strftime("%A %d %B %Y")
    except Exception:
        readable_date = date

    await callback.message.answer(
        f"✅ نوبت شما ثبت شد.\n"
        f"💈 خدمت: {service}\n"
        f"📅 تاریخ: {readable_date}\n"
        f"🕐 ساعت: {time}",
        reply_markup=keyboard.main_keyboard()
    )

    await state.clear()
    await callback.answer()