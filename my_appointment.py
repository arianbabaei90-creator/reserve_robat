from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

import database
import keyboard

router = Router()


@router.message(F.text == "📋 نوبت های من")
async def my_appointments(message: Message):
    user_id = message.from_user.id
    appointments = await database.get_user_informaition(user_id)

    if not appointments:
        await message.answer("📋 شما هیچ نوبتی ندارید.")
        return

    await message.answer("📋 نوبت‌های شما:")

    for appointment_id, service, date, time, status in appointments:
        text = (
            f"💈 خدمت: {service}\n"
            f"📅 تاریخ: {date}\n"
            f"🕐 ساعت: {time}\n"
            f"📌 وضعیت: {status}\n"
        )
        if status == "active":
            await message.answer(text, reply_markup=keyboard.cancel(appointment_id))
        else:
            await message.answer(text)


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_handler(callback: CallbackQuery):
    appointment_id = int(callback.data.split(":")[1])
    user_id = callback.from_user.id

    success = await database.cancel_appointment(appointment_id, user_id)

    if not success:
        await callback.answer("امکان لغو این نوبت وجود ندارد", show_alert=True)
        return

    await callback.message.edit_text("❌ نوبت شما با موفقیت لغو شد.")
    await callback.answer()