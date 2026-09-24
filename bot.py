import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@MaraghehOnlineCom")
CHANNEL_URL = os.getenv(
    "CHANNEL_URL",
    "https://t.me/MaraghehOnlineCom"
)

ADMIN_USERNAME = "@montazr313"

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# -------------------------
# بررسی عضویت در کانال
# -------------------------
async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL,
            user_id=user_id
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception as e:
        logging.error(f"Membership check error: {e}")
        return False


# -------------------------
# دکمه عضویت
# -------------------------
def join_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 عضویت در کانال مراغه آنلاین",
                    url=CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ بررسی عضویت",
                    callback_data="check_join"
                )
            ]
        ]
    )


# -------------------------
# منوی اصلی
# -------------------------
def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 کانال مراغه آنلاین",
                    url=CHANNEL_URL
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 شرایط تبلیغات",
                    callback_data="ads"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 ارتباط با مدیر",
                    url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏙️ ارسال مشکلات شهری",
                    callback_data="problems"
                )
            ]
        ]
    )


# -------------------------
# /start
# -------------------------
@dp.message(CommandStart())
async def start_handler(message: Message):

    if not await is_member(message.from_user.id):

        await message.answer(
            "🔔 برای استفاده از ربات ابتدا باید عضو کانال مراغه آنلاین شوید.\n\n"
            "بعد از عضویت روی «بررسی عضویت» بزنید.",
            reply_markup=join_keyboard()
        )
        return

    await message.answer(
        "سلام 👋\n\n"
        "به ربات مراغه آنلاین خوش آمدید 🌹\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=main_keyboard()
    )


# -------------------------
# بررسی دوباره عضویت
# -------------------------
@dp.callback_query(F.data == "check_join")        return member.status in {"member", "administrator", "creator"} or (
            member.status == "restricted" and getattr(member, "is_member", False)
        )
    except Exception:
        logging.exception("Membership check failed")
        return False


async def show_gate(target):
    text = (
        "📰 <b>مراغه آنلاین</b>\n\n"
        "برای استفاده از ربات، ابتدا عضو کانال مراغه آنلاین شوید.\n\n"
        "پس از عضویت، روی «عضو شدم» بزنید."
    )
    if isinstance(target, Message):
        await target.answer(text, reply_markup=join_keyboard())
    else:
        await target.message.edit_text(text, reply_markup=join_keyboard())


@dp.message(CommandStart())
async def start(message: Message):
    if await is_member(message.from_user.id):
        await message.answer(
            "✅ عضویت شما تأیید شد.\n\n"
            "به ربات مراغه آنلاین خوش آمدید.\n"
            "خدمات ربات را می‌توانید از منوی پایین دریافت کنید."
        )
    else:
        await show_gate(message)


@dp.callback_query(F.data == "check_join")
async def check_join(callback: CallbackQuery):
    if await is_member(callback.from_user.id):
        await callback.answer("عضویت تأیید شد ✅")
        await callback.message.edit_text(
            "✅ <b>عضویت شما تأیید شد.</b>\n\n"
            "به ربات مراغه آنلاین خوش آمدید.\n"
            "از اینجا می‌توانید خدمات ربات را دریافت کنید."
        )
    else:
        await callback.answer(
            "هنوز عضویت شما تأیید نشده است. ابتدا عضو کانال شوید.",
            show_alert=True
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
