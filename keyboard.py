from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def admin_keyboard():
    return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="📅 رزرو نوبت"),
                    KeyboardButton(text="📋 نوبت های من"),
                    KeyboardButton(text="پنل مدیریت")
                ],
            ],
            resize_keyboard=True
        
    )
def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                
                    KeyboardButton(text="📅 رزرو نوبت"),
                    KeyboardButton(text="📋 نوبت های من")
            ]
        ],
        resize_keyboard=True
        
    )
def manager():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="گزارش امروز",callback_data="گزارش امروز"),
                InlineKeyboardButton(text="گزارش این ماه",callback_data="گزارش این ماه")
    
            ],
            [
                InlineKeyboardButton(text="کاربران",callback_data="users")
                
            ]
           
        ]
    )

def cancel(appointment_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
              [
                InlineKeyboardButton(text="❌ لغو نوبت",callback_data=f"cancel:{appointment_id}")
              ]
        ]
    )
def service():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💇 اصلاح مو",
                    callback_data="service:hair"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧔 اصلاح صورت",
                    callback_data="service:beard"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💈 مو + صورت",
                    callback_data="service:hair,beard"
                )
            ]
        ]
    )
import jdatetime
from datetime import timedelta

def date():
    keyboard = []
    today = jdatetime.date.today()

    # نام روزهای هفته به فارسی
    week_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه"]

    row = []
    for i in range(7):
        d = today + timedelta(days=i)
        # نام روز هفته در jdatetime: 0 = شنبه ... 6 = جمعه
        day_name = week_days[d.weekday()]
        # تاریخ به فرمت 1403-05-12
        date_str = d.strftime("%Y-%m-%d")

        # اگر امروز بود بنویس "امروز"
        label = f"{day_name} {d.day}/{d.month}"
        if i == 0:
            label = f"امروز {d.day}/{d.month}"
        elif i == 1:
            label = f"فردا {d.day}/{d.month}"

        row.append(
            InlineKeyboardButton(
                text=label,
                callback_data=f"data:{date_str}"
            )
        )

        # هر ردیف ۲ دکمه
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
def time():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="10.00",
                    callback_data="time:10.00"
                ),

                InlineKeyboardButton(
                    text="11.00",
                    callback_data="time:11.00"
                                )
            ],
            [
                InlineKeyboardButton(
                    text="12.00",
                    callback_data="time:12.00"
                                ),
                
                InlineKeyboardButton(
                    text="14.00",
                    callback_data="time:14.00"
                                                )
            ],
        ])
