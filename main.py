from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توکن ربات
TOKEN = "7723810377:AAFd8AvyVudbGJwT-BjqIOM_EtMh4hNZBzo"

# آیدی تلگرام ادمین بدون @
ADMIN_USERNAME = "emihesi"

# اطلاعات کتاب‌ها
books = {
    "book1": {
        "title": "راهنمای جامع درمان در گفتاردرمانی",
        "description": """راهنمای جامع ارزیابی و درمان تمام اختلالات گفتاردرمانی
یک مرجع کامل، کاربردی و دسته‌بندی‌شده برای ارزیابی و درمان تمام اختلالات گفتار و زبان، شامل نکات کلینیکی، جدول‌های کاربردی، مراحل درمانی، و رویکردهای روز دنیا.
مناسب برای گفتاردرمانگرانی که می‌خوان سریع، دقیق و علمی تصمیم‌گیری کنند.
قیمت با تخفیف ویژه: ۱۹۹ هزار تومان""",
        "demo_file": "دمو_راهنمای_جامع_درمان_در_گفتاردرمانی.pdf"
    },
    "book2": {
        "title": "پکیج تمرینات روزانه برای درمان آپراکسی گفتار در کودکان",
        "description": """پکیج تمرینات روزانه برای آپراکسی گفتار کودکان
راهنمای کامل، مرحله‌به‌مرحله و قابل اجرا برای تمرین روزانه کودکان مبتلا به آپراکسی گفتار. شامل ۸ هفته تمرین هدفمند، توضیح ساده، و بدون نیاز به ابزار خاص.
قیمت با تخفیف ویژه: ۹۹ هزار تومان""",
        "demo_file": "دمو_پکیج_تمرینات_روزانه_برای_درمان_آپراکسی_گفتار_در_کودکان.pdf"
    },
    "book3": {
        "title": "چک لیست کامل ارزیابی واج شناسی",
        "description": """چک‌لیست کامل ارزیابی واج‌شناسی (Phonological Processes)
مناسب برای ارزیابی دقیق و حرفه‌ای فرآیندهای واجی در کودکان، به زبان ساده و قابل استفاده در جلسات درمان. شامل توضیح تئوری، مثال‌های بالینی، فرم‌های چک‌لیست و پرسش‌نامه برای والدین.
قیمت با تخفیف ویژه: ۹۹ هزار تومان""",
        "demo_file": "دمو_چک‌_لیست_کامل_ارزیابی_واج_‌شناسی.pdf"
    }
}

# فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(book["title"], callback_data=key)] for key, book in books.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! یکی از کتاب‌های زیر رو انتخاب کن:", reply_markup=reply_markup)

# مدیریت کلیک روی دکمه کتاب‌ها
async def book_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    key = query.data
    if key in books:
        book = books[key]
        
        # ارسال توضیح کتاب
        await query.message.reply_text(book["description"])

        # ارسال فایل دمو
        try:
            with open(book["demo_file"], "rb") as demo:
                await query.message.reply_document(InputFile(demo))
        except FileNotFoundError:
            await query.message.reply_text("فایل دمو پیدا نشد. لطفاً بررسی شود.")

        # ارسال دکمه خرید
        buy_link = f"https://t.me/{ADMIN_USERNAME}?start={book['title'].replace(' ', '_')}"
        keyboard = [[InlineKeyboardButton("📥 خرید این کتاب", url=buy_link)]]
        await query.message.reply_text("برای خرید، روی دکمه زیر کلیک کن:", reply_markup=InlineKeyboardMarkup(keyboard))

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(book_detail))
    print("ربات اجرا شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
