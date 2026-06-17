import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from downloader import download_instagram_video
import tempfile

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Salom! 👋\n\n"
        "Instagram video yoki Reel havolasini yuboring — "
        "men uni yuklab, sizga yuboraman.\n\n"
        "📌 Misol:\n"
        "https://www.instagram.com/reel/ABC123/\n\n"


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 <b>Foydalanish yo'riqnomasi</b>\n\n"
        "1. Instagram'dan video yoki Reel havolasini nusxalang\n"
        "2. Havolani menga yuboring\n"
        "3. Video yuklab bo'lgach, avtomatik yuboriladi\n\n"
        "⚠️ <b>Eslatma:</b>\n"
        "• Faqat ochiq (public) profillar ishlaydi\n"
        "• Maksimal video hajmi: 50 MB\n"
        "• Yuklab olish 10–30 soniya vaqt olishi mumkin",
        parse_mode="HTML"
    )


@dp.message()
async def handle_link(message: Message):
    text = message.text.strip() if message.text else ""

    # Instagram havolasini tekshirish
    if "instagram.com" not in text:
        await message.answer(
            "❌ Instagram havolasi emas.\n\n"
            "Iltimos, quyidagi formatda havola yuboring:\n"
            "https://www.instagram.com/reel/..."
        )
        return

    wait_msg = await message.answer("⏳ Video yuklanmoqda, biroz kuting...")

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info(f"Yuklab olish boshlandi: {text}")

            file_path = await asyncio.get_event_loop().run_in_executor(
                None, download_instagram_video, text, tmpdir
            )

            if file_path and os.path.exists(file_path):
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                logger.info(f"Fayl yuklab olindi: {file_path} ({file_size_mb:.1f} MB)")

                if file_size_mb > 50:
                    await wait_msg.edit_text(
                        f"❌ Video hajmi juda katta ({file_size_mb:.1f} MB).\n"
                        "Telegram 50 MB dan katta fayllarni qabul qilmaydi."
                    )
                    return

                video = FSInputFile(file_path)
                await message.answer_video(
                    video=video,
                    caption="✅ Mana sizning videongiz!\n\n🤖 @YourBotUsername"
                )
                await wait_msg.delete()
            else:
                await wait_msg.edit_text(
                    "❌ Videoni yuklab bo'lmadi.\n\n"
                    "Sabablari:\n"
                    "• Profil yopiq (private) bo'lishi mumkin\n"
                    "• Havola noto'g'ri yoki eskirgan\n"
                    "• Instagram vaqtincha bloklagan\n\n"
                    "Keyinroq qayta urinib ko'ring."
                )

    except Exception as e:
        logger.error(f"Xatolik: {e}", exc_info=True)
        await wait_msg.edit_text(
            "❌ Kutilmagan xatolik yuz berdi.\n"
            "Iltimos, keyinroq qayta urinib ko'ring."
        )


async def main():
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
