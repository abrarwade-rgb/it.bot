import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = "8953275408:AAGZDn0C7n9nKOSdFQmsw67r1bzDWiyGh6Q"
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()  # لحذف أي ربط ويبهوك قديم وإيقاف الإعلانات المزعجة نهائياً

# --- 1. سيرفر الـ Flask لإبقاء البوت مستيقظاً على Render ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


# --- 2. القوائم والأزرار الرئيسية والفرعية ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("🎓 جامعة الجند IT مستوى ثاني 2026/2027")
    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        "مرحباً بك يا أبرار في بوت دليل تقنية المعلومات - جامعة الجند 💙✨\nاختر من الأدناه:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id

    if text == "🎓 جامعة الجند IT مستوى ثاني 2026/2027":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_level1 = types.KeyboardButton("📚 مستوى أول")
        btn_level2 = types.KeyboardButton("🔒 مستوى ثاني")
        btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
        markup.add(btn_level1, btn_level2, btn_home)
        bot.send_message(chat_id, "اختر المستوى الدراسي:", reply_markup=markup)

    elif text == "🏠 القائمة الرئيسية":
        send_welcome(message)

    elif text == "🔒 مستوى ثاني":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_back = types.KeyboardButton("رجوع")
        markup.add(btn_back)
        bot.send_message(
            chat_id,
            "⚠️ الترم الثاني والمستوى الثاني غير متوفر حالياً، لم يتم البدء فيه بعد، يتم تجهيز محتوى الترم.",
            reply_markup=markup
        )

    elif text == "رجوع":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_level1 = types.KeyboardButton("📚 مستوى أول")
        btn_level2 = types.KeyboardButton("🔒 مستوى ثاني")
        btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
        markup.add(btn_level1, btn_level2, btn_home)
        bot.send_message(chat_id, "أهلاً بك، اختر المستوى:", reply_markup=markup)

    elif text == "📚 مستوى أول" or text == "العودة للمقررات":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_m1 = types.KeyboardButton("⚡ تصميم منطقي رقمي (د. عبد الرحمن سعيد)")
        btn_m2 = types.KeyboardButton("💻 مقدمة قواعد بيانات (د. بشير الطيار)")
        btn_m3 = types.KeyboardButton("🔌 مبادئ الدوائر الكهربائية (د. مروان العسلي)")
        btn_m4 = types.KeyboardButton("🏗️ هياكل البيانات والخوارزميات (د. محمد سلطان)")
        btn_m5 = types.KeyboardButton("📐 تحليل وتصميم النظم (د. عبد الرحمن سعيد)")
        btn_m6 = types.KeyboardButton("📈 الإحصاء والاحتمالات (د. رياض الشرعبي)")
        btn_m7 = types.KeyboardButton("📊 مبادئ المحاسبة (د. ذي يزن)")
        btn_m8 = types.KeyboardButton("📅 جدول المحاضرات")
        
        btn_back = types.KeyboardButton("رجوع")
        btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
        
        markup.add(btn_m1, btn_m2, btn_m3, btn_m4, btn_m5, btn_m6, btn_m7, btn_m8)
        markup.row(btn_back, btn_home)
        
        bot.send_message(
            chat_id,
            "📚 مقررات مستوى أول - اختر المقرر المطلوب:",
            reply_markup=markup
        )

    elif "تصميم منطقي رقمي" in text:
        send_course_menu(chat_id, "تصميم منطقي رقمي (د. عبد الرحمن سعيد)", has_practical=True)
    elif "مقدمة قواعد بيانات" in text:
        send_course_menu(chat_id, "مقدمة قواعد بيانات (د. بشير الطيار)", has_practical=True)
    elif "مبادئ الدوائر الكهربائية" in text:
        send_course_menu(chat_id, "مبادئ الدوائر الكهربائية (د. مروان العسلي)", has_practical=True)
    elif "هياكل البيانات والخوارزميات" in text:
        send_course_menu(chat_id, "هياكل البيانات والخوارزميات (د. محمد سلطان)", has_practical=True)
    elif "تحليل وتصميم النظم" in text:
        send_course_menu(chat_id, "تحليل وتصميم النظم (د. عبد الرحمن سعيد)", has_practical=True)
    elif "الإحصاء والاحتمالات" in text or "مبادئ المحاسبة" in text:
        send_course_menu(chat_id, text, has_practical=False)

    elif text == "📅 جدول المحاضرات":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(types.KeyboardButton("العودة للمقررات"), types.KeyboardButton("🏠 القائمة الرئيسية"))
        bot.send_message(chat_id, "📅 هنا سيتم إدراج جدول المحاضرات الدراسية.", reply_markup=markup)

    elif "ملزمة المقرر" in text or "صور المحاضرات" in text or "ملخص المقرر" in text or "نماذج اختبارات" in text or "العملي" in text:
        bot.send_message(chat_id, f"📁 جلب المحتوى لـ: ({text})\n*(قريباً سيتم رفع الملفات الخاصة بهذا القسم هنا)*")

def send_course_menu(chat_id, course_name, has_practical=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    
    btn_mlazem = types.KeyboardButton("📖 ملزمة المقرر")
    btn_photos = types.KeyboardButton("🖼️ صور المحاضرات")
    btn_summary = types.KeyboardButton("📝 ملخص المقرر")
    btn_exams = types.KeyboardButton("📋 نماذج اختبارات")
    
    markup.add(btn_mlazem, btn_photos, btn_summary, btn_exams)
    
    if has_practical:
        btn_practical = types.KeyboardButton("⚙️ العملي")
        markup.add(btn_practical)
        
    btn_back = types.KeyboardButton("العودة للمقررات")
    btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
    markup.row(btn_back, btn_home)
    
    bot.send_message(chat_id, f"📌 اختر المحتوى المطلوب لمادة: *{course_name}*", parse_mode="Markdown", reply_markup=markup)


# --- 3. تشغيل السيرفر والبوت معاً ---
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    print("Bot is running...")
    bot.infinity_polling()
    
