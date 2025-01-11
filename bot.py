import telebot
import subprocess
import sys

# نصب خودکار کتابخانه‌های مورد نیاز
required_libraries = ["pytelegrambotapi", "deep_translator"]
for lib in required_libraries:
    try:
        __import__(lib)
    except ImportError:
        print(f"در حال نصب کتابخانه {lib}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

from deep_translator import GoogleTranslator
from line import convert_to_cuneiform, convert_to_pahlavi, convert_to_manichaean, convert_to_hieroglyph, text_to_linear_b_optimized

# توکن ربات را از BotFather دریافت کرده و اینجا جایگزین کنید
BOT_TOKEN = "token"

# ایجاد نمونه ربات
bot = telebot.TeleBot(BOT_TOKEN)

# پیام خوش‌آمدگویی در هنگام شروع چت با ربات
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_message = (
        "**سلام و عرض ادب! 👋**\n\n"
        "به ربات تبدیل متن به خطوط باستانی خوش آمدید. ✨\n"
        "این ربات می‌تواند متن‌های شما را به خطوط باستانی مختلف تبدیل کند:\n"
        "- خط میخی\n"
        "- خط پهلوی\n"
        "- خط مانوی\n"
        "- خط هیروگلیف\n"
        "- خط عبری\n"
        "- خط میکنی (Linear B)\n\n"
        "**برای شروع، متن مورد نظر خود را ارسال کنید.** 😊"
    )
    bot.reply_to(message, welcome_message, parse_mode="Markdown")

# پاسخ به پیام‌های کاربر و تبدیل به خطوط باستانی
@bot.message_handler(func=lambda message: True)
def convert_text_to_ancient_lines(message):
    try:
        input_text = message.text.strip()

        bot.reply_to(message, "**در حال تبدیل متن شما به خطوط باستانی...**", parse_mode="Markdown")

        # تبدیل متن به خطوط باستانی مختلف
        cuneiform_output = convert_to_cuneiform(input_text)
        pahlavi_output = convert_to_pahlavi(input_text)
        manavi_output = convert_to_manichaean(input_text)
        hieroglyph = convert_to_hieroglyph(input_text)
        hw = GoogleTranslator(source='auto', target='iw').translate(input_text)
        linear_b_optimized = text_to_linear_b_optimized(input_text)

        # ایجاد پاسخ نهایی
        response = (
            "**نتیجه تبدیل متن شما:**\n\n"
            f"📜 **متن به خط میخی:**\n{cuneiform_output}\n\n"
            f"📜 **متن به خط پهلوی:**\n{pahlavi_output}\n\n"
            f"📜 **متن به خط مانوی:**\n{manavi_output}\n\n"
            f"📜 **متن به خط هیروگلیف:**\n{hieroglyph}\n\n"
            f"📜 **متن به خط عبری:**\n{hw}\n\n"
            f"📜 **متن به خط میکنی (Linear B):**\n{linear_b_optimized}\n\n"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"خطایی رخ داد: {e}")

# اجرا کردن ربات
if __name__ == "__main__":
    print("ربات در حال اجراست...")
    bot.polling()
