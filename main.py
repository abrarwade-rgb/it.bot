import os
import threading
from flask import Flask
import telebot
from telebot import types

# ----------------------------------------------------
# 1. إعداد سيرفر Flask لضمان التشغيل الدائم 24/7
# ----------------------------------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "IT Assistant Bot is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ----------------------------------------------------
# 2. إعداد بوت تليجرام
# ----------------------------------------------------
# ضع التوكن الخاص ببوتك هنا
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ضع_التوكن_الخاص_بكبوتك_هنا")
bot = telebot.TeleBot(BOT_TOKEN)

# --- القائمة الرئيسية للمواد ---
def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("📊 Dr. Dhi Yazan - مبادئ محاسبة")
    btn2 = types.KeyboardButton("💡 Dr. Abdulrahman - تصميم منطقي رقمي")
    btn3 = types.KeyboardButton("📈 Dr. Riyad - الإحصاء والاحتمالات")
    btn4 = types.KeyboardButton("🏗️ Dr. Mohammed - هياكل بيانات")
    btn5 = types.KeyboardButton("💾 Dr. Basher - مقدمة قواعد بيانات")
    btn6 = types.KeyboardButton("⚡ Dr. Shuaib - دوائر كهربائية وإلكترونية")
    btn7 = types.KeyboardButton("📐 Dr. Abdulrahman - تحليل وتصميم نظم")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    
    text = "أهلاً بك في دليل IT Assistant 🎓✨\nاختر المادة لعرض الملازم والملخصات:"
    bot.send_message(chat_id, text, reply_markup=markup)

# ----------------------------------------------------
# 3. معالجة الأوامر والرسائل
# ----------------------------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    # --- 1️⃣ مادة قواعد البيانات ---
    if text == "💾 Dr. Basher - مقدمة قواعد بيانات":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("📚 ملازم قواعد البيانات")
        btn2 = types.KeyboardButton("📝 ملخصات قواعد البيانات")
        btn3 = types.KeyboardButton("🖼️ صور الشرح")
        btn_back = types.KeyboardButton("🏠 القائمة الرئيسية")
        
        markup.add(btn1, btn2, btn3, btn_back)
        bot.send_message(chat_id, "📁 قسم مقدمة قواعد البيانات - اختر ما تريد:", reply_markup=markup)

    elif text == "📚 ملازم قواعد البيانات":
        bot.send_message(chat_id, "جاري إرسال ملازم قواعد البيانات... 📄")
        
        # ⚠️ استبدلي النصين أدناه بـ file_id الحقيقي عند استخراجه من GetFileIdBot
        FILE_ID_1 = "استبدلي_هذا_بالـfile_id_للملزمة_الأولى"
        FILE_ID_2 = "استبدلي_هذا_بالـfile_id_للملزمة_الثانية"
        
        try:
            bot.send_document(chat_id, FILE_ID_1, caption="📄 ملزمة قواعد البيانات - الجزء 1")
            bot.send_document(chat_id, FILE_ID_2, caption="📄 ملزمة قواعد البيانات - الجزء 2")
        except Exception as e:
            bot.send_message(chat_id, "⚠️ لم يتم إضافة file_id الصحيح للملازم بعد.")

    # --- 2️⃣ العودة للقائمة الرئيسية ---
    elif text == "🏠 القائمة الرئيسية":
        send_main_menu(chat_id)

    # --- 3️⃣ باقي المواد (قوالب جاهزة للقوائم الفرعية) ---
    elif "مبادئ محاسبة" in text or "تصميم منطقي" in text or "الإحصاء" in text or "هياكل بيانات" in text or "دوائر كهربائية" in text or "تحليل وتصميم نظم" in text:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("📚 الملازم")
        btn2 = types.KeyboardButton("📝 الملخصات")
        btn_back = types.KeyboardButton("🏠 القائمة الرئيسية")
        markup.add(btn1, btn2, btn_back)
        
        bot.send_message(chat_id, f"اختر المطلوب لمادة: {text}", reply_markup=markup)

# ----------------------------------------------------
# 4. تشغيل السيرفر والبوت معا
# ----------------------------------------------------
if __name__ == "__main__":
    # تشغيل سيرفر Flask في الخفاء (Thread)
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # تشغيل البوت
    print("Bot is running...")
    bot.infinity_polling()
