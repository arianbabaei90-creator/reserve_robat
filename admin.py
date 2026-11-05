from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

import database
import keyboard
from config import ADMIN_ID

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


@router.message(F.text == "پنل مدیریت")
async def management(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("دسترسی ندارید")
        return
    await message.answer("یکی از گزینه ها رو وارد کنید", reply_markup=keyboard.manager())


@router.callback_query(F.data == "today_status")
async def today_status(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("دسترسی ندارید", show_alert=True)
        return

    status = await database.today_status()
    if not status:
        await callback.message.answer("نوبتی امروز یافت نشد")
        await callback.answer()
        return

    total, active, cancelled = status
    await callback.message.answer(
        f"📊 گزارش امروز\n\n"
        f"🔢 کل نوبت‌ها: {total}\n"
        f"🟢 نوبت‌های فعال: {active}\n"
        f"🔴 نوبت‌های لغوشده: {cancelled}"
    )
    await callback.answer()


@router.callback_query(F.data == "month_status")
async def month_status(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("دسترسی ندارید", show_alert=True)
        return

    status = await database.month_status()
    if not status:
        await callback.message.answer("نوبتی یافت نشد")
        await callback.answer()
        return

    total, active, cancelled = status
    await callback.message.answer(
        f"📊 گزارش این ماه\n\n"
        f"🔢 کل نوبت‌ها: {total}\n"
        f"🟢 نوبت‌های فعال: {active}\n"
        f"🔴 نوبت‌های لغوشده: {cancelled}"
    )
    await callback.answer()


@router.callback_query(F.data == "users")
async def show_users(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("دسترسی ندارید", show_alert=True)
        return

    users = await database.users_information()
    if not users:
        await callback.message.answer("کاربری یافت نشد")
        await callback.answer()
        return

    lines = ["👥 لیست کاربران:\n"]
    for user_id, name, phone, count in users:
        lines.append(
            f"👤 {name}\n"
            f"📱 {phone}\n"
            f"📅 تعداد نوبت‌ها: {count}\n"
        )

    full_text = "\n".join(lines)
    chunk_size = 4000
    for i in range(0, len(full_text), chunk_size):
        await callback.message.answer(full_text[i:i + chunk_size])

    await callback.answer()