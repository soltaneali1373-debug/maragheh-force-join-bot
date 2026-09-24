import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@MaraghehOnline_Com")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/MaraghehOnline_Com")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required")

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


def join_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 عضویت در مراغه آنلاین", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ عضو شدم", callback_data="check_join")]
    ])


async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        return member.status in {"member", "administrator", "creator"} or (
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
