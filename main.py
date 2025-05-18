from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from web import keep_alive

# توکن ربات
TOKEN = "7723810377:AAGAQ6JRI4Z5ZHRGmXsasPJqEakhGreHqwA"

# آیدی تلگرام ادمین بدون @
ADMIN_USERNAME = "emihesi"

# زبان کاربران
user_language = {}

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
        "title": "راهنمای جامع درمان اختلالات صوت",
        "description": """این کتاب کامل‌ترین راهنمای گفتاردرمانگران برای تاریخچه‌گیری، ارزیابی و درمان اختلالات صوت است.
در این کتاب، فرم‌ها و چک‌لیست‌های کاربردی برای ارزیابی دقیق اختلالات صوت قرار داده شده و تمرینات درمانی ساده و مرحله‌به‌مرحله همراه با نکات مهم بالینی ارائه شده است.
مناسب گفتاردرمانگرانی که می‌خواهند در زمینه درمان اختلالات صوت تخصص و تسلط بیشتری پیدا کنند.

قیمت با تخفیف: ۱۴۴,۰۰۰ تومان""",
        "demo_file": "دمو_اختلالات_صوت.pdf"
    },
    "book3": {
        "title": "راهنمای جامع عقب ماندگی ذهنی",
        "description": """این کتاب یه راهنمای کامل و ساده است برای همه کسانی که می‌خوان عقب‌ماندگی ذهنی رو بهتر بشناسن، درست ارزیابی کنن و برنامه درمانی مناسب طراحی کنن. با زبان راحت و قابل فهم، مراحل تاریخچه‌گیری، ارزیابی و درمان رو مرحله به مرحله توضیح داده تا هم والدین و هم متخصصان گفتاردرمانی بتونن راحت‌تر کمک کنن.
این کتاب بهترین همراه برای بهبود کیفیت زندگی کودکان با نیازهای ویژه است.

قیمت با تخفیف: ۱۳۵,۰۰۰ تومان""",
        "demo_file": "دمو_راهنمای_جامع_عقب_ماندگی_ذهنی.pdf"
    }
}

# شروع با انتخاب زبان
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("فارسی", callback_data="lang_fa"),
         InlineKeyboardButton("English", callback_data="lang_en")]
    ]
    await update.message.reply_text("لطفاً زبان مورد نظر را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

# مدیریت انتخاب زبان
async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == "lang_fa":
        user_language[user_id] = "fa"
        await query.answer()
        await query.message.reply_text("زبان فارسی انتخاب شد. لطفاً یکی از کتاب‌های زیر را انتخاب کن:")

        keyboard = [[InlineKeyboardButton(book["title"], callback_data=key)] for key, book in books.items()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("کتاب‌ها:", reply_markup=reply_markup)

    elif query.data == "lang_en":
        user_language[user_id] = "en"
        await query.answer()
        await query.message.reply_text("English content coming soon...")

# نمایش توضیحات و دمو کتاب
async def book_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    key = query.data

    if key in books:
        book = books[key]
        await query.message.reply_text(book["description"])

        try:
            with open(book["demo_file"], "rb") as demo:
                await query.message.reply_document(InputFile(demo))
        except FileNotFoundError:
            await query.message.reply_text("فایل دمو پیدا نشد. لطفاً بررسی شود.")

        # دکمه خرید
        buy_keyboard = [[InlineKeyboardButton("خرید کتاب", callback_data=f"buy_{key}")]]
        await query.message.reply_text("برای خرید، روی دکمه‌ی زیر کلیک کن:", reply_markup=InlineKeyboardMarkup(buy_keyboard))

# سیستم خرید کتاب
async def buy_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("محبت کنید مبلغ مورد نظر را به شماره کارت زیر واریز کنید:\n6037991922825686\nبه نام امیرحسین عزیزی فروتقه")

    buy_link = f"https://t.me/{ADMIN_USERNAME}"
    keyboard = [[InlineKeyboardButton("ارسال رسید خرید", url=buy_link)]]
    await query.message.reply_text("برای اشتراک رسید خرید، روی دکمه زیر کلیک کن:", reply_markup=InlineKeyboardMarkup(keyboard))

# اجرای ربات
def main():
    keep_alive()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_language, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(buy_book, pattern="^buy_"))
    app.add_handler(CallbackQueryHandler(book_detail))
    print("ربات اجرا شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
