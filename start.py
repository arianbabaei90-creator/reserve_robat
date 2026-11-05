from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboard import main_keyboard,admin_keyboard
from config import ADMIN_ID
import database
router = Router()

@router.message(CommandStart())
async def start_handler(message:Message):
    name=message.from_user.full_name
    user_id=message.from_user.id
    if user_id==ADMIN_ID:
        kb=admin_keyboard()
    else:
        kb=main_keyboard()
        await database.add_user(name,user_id)
        await message.answer(
                f"سلام {name}\n"
                "به ربات رزرو نوبت آرایشگاه خوش آمدید",
                reply_markup=kb
            )
        
    
