import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

# --- 1. سيرفر الـ Flask لإبقاء البوت مستيقظاً على Render ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))


# --- متغير لحفظ المقرر الحالي لكل مستخدم ---
user_course = {}


# --- 2. القوائم والأزرار الرئيسية والفرعية ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("🎓 جامعة الجند IT مستوى ثاني 2026/2027")
    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        "مرحباً بك في بوت دليل تقنية المعلومات - جامعة الجند 💙✨\nاختر من الأدناه:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    text = message.text
    chat_id = message.chat.id

    if text == "🎓 جامعة الجند IT مستوى ثاني 2026/2027":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_term1 = types.KeyboardButton("📚 ترم أول")
        btn_term2 = types.KeyboardButton("🔒 ترم ثاني")
        btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
        markup.add(btn_term1, btn_term2, btn_home)
        bot.send_message(chat_id, "اختر الترم الدراسي:", reply_markup=markup)

    elif text == "🏠 القائمة الرئيسية":
        send_welcome(message)

    elif text == "🔒 ترم ثاني":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_back = types.KeyboardButton("رجوع")
        markup.add(btn_back)
        bot.send_message(
            chat_id,
            "⚠️ الترم الثاني غير متوفر حالياً، لم يتم البدء فيه بعد، يتم تجهيز محتوى الترم.",
            reply_markup=markup
        )

    elif text == "رجوع":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_term1 = types.KeyboardButton("📚 ترم أول")
        btn_term2 = types.KeyboardButton("🔒 ترم ثاني")
        btn_home = types.KeyboardButton("🏠 القائمة الرئيسية")
        markup.add(btn_term1, btn_term2, btn_home)
        bot.send_message(chat_id, "أهلاً بك، اختر الترم الدراسي:", reply_markup=markup)

    elif text == "📚 ترم أول" or text == "العودة للمقررات":
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
            "📚 مقررات الترم الأول - اختر المقرر المطلوب:",
            reply_markup=markup
        )

    elif "تصميم منطقي رقمي" in text:
        user_course[chat_id] = "logic"
        send_course_menu(chat_id, "تصميم منطقي رقمي (د. عبد الرحمن سعيد)", has_practical=True)
    elif "مقدمة قواعد بيانات" in text:
        user_course[chat_id] = "db"
        send_course_menu(chat_id, "مقدمة قواعد بيانات (د. بشير الطيار)", has_practical=True)
    elif "مبادئ الدوائر الكهربائية" in text:
        user_course[chat_id] = "circuits"
        send_course_menu(chat_id, "مبادئ الدوائر الكهربائية (د. مروان العسلي)", has_practical=True)
    elif "هياكل البيانات والخوارزميات" in text:
        user_course[chat_id] = "ds"
        send_course_menu(chat_id, "هياكل البيانات والخوارزميات (د. محمد سلطان)", has_practical=True)
    elif "تحليل وتصميم النظم" in text:
        user_course[chat_id] = "sad"
        send_course_menu(chat_id, "تحليل وتصميم النظم (د. عبد الرحمن سعيد)", has_practical=False)
    elif "الإحصاء والاحتمالات" in text or "مبادئ المحاسبة" in text:
        user_course[chat_id] = "other"
        send_course_menu(chat_id, text, has_practical=False)

    # 📅 زر جدول المحاضرات (يرسل الصورة محلياً فوراً)
    elif text == "📅 جدول المحاضرات":
        try:
            with open('table.png', 'rb') as photo:
                bot.send_photo(
                    chat_id, 
                    photo, 
                    caption="📅 جدول المحاضرات الدراسية\n💙 دفعة IT - جامعة الجند"
                )
        except Exception as e:
            bot.send_message(chat_id, "📅 جدول المحاضرات الدراسية (تأكد من رفع صورة table.png في المستودع)")

    # 📖 ملزمة المقرر (ترسل ملازم المادة المختارة محلياً في الشات)
    elif text == "📖 ملزمة المقرر":
        current = user_course.get(chat_id)

        if current == "db":
            bot.send_message(chat_id, "📖 جاري إرسال ملازم مقرر قواعد البيانات...")
            try:
                with open('database_part1.pptx', 'rb') as f1:
                    bot.send_document(chat_id, f1, caption="📖 ملزمة مقدمة قواعد البيانات (الجزء الأول)\nد/ بشير الطيار\n💙 دفعة IT - جامعة الجند")
                with open('database_part2.pptx', 'rb') as f2:
                    bot.send_document(chat_id, f2, caption="📖 ملزمة مقدمة قواعد البيانات (الجزء الثاني)\nد/ بشير الطيار\n💙 دفعة IT - جامعة الجند")
            except Exception as e:
                bot.send_message(chat_id, "⚠️ تذكير: تأكد من رفع ملفات الباوربوينت (database_part1.pptx و database_part2.pptx) في جيت هاب.")

        elif current == "sad":
            bot.send_message(chat_id, "📖 جاري إرسال ملازم مقرر تحليل وتصميم النظم (من المحاضرة الأولى إلى السابعة)...")
            sad_lectures = [
                ("lecture1.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة الأولى\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("lecture2.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة الثانية\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("Lecture3.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة الثالثة\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("Lecture4.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة الرابعة\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("Lecture5.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة الخامسة\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("Lecture6.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة السادسة\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
                ("Lecture7.ppt", "📖 ملزمة تحليل وتصميم النظم — المحاضرة السابعة\nد/ عبد الرحمن سعيد\n💙 دفعة IT - جامعة الجند"),
            ]
            for filename, caption in sad_lectures:
                try:
                    with open(filename, 'rb') as f:
                        bot.send_document(chat_id, f, caption=caption)
                except FileNotFoundError:
                    bot.send_message(chat_id, f"⚠️ تنبيه: الملف ({filename}) غير مرفوع حالياً في جيت هاب.")
                except Exception as e:
                    bot.send_message(chat_id, f"⚠️ حدث خطأ أثناء إرسال ({filename}): {e}")

        elif current == "circuits":
            bot.send_message(chat_id, "📖 جاري إرسال ملزمة مقرر مبادئ الدوائر الكهربائية...")
            try:
                with open('circuits1.pdf', 'rb') as fc1:
                    bot.send_document(
                        chat_id,
                        fc1,
                        caption="📖 Fundamentals of Electrical and Electronic Circuits (2026)\nد/ مروان العسلي\n💙 دفعة IT - جامعة الجند"
                    )
            except FileNotFoundError:
                bot.send_message(chat_id, "⚠️ تنبيه: الملف (circuits1.pdf) غير مرفوع حالياً في جيت هاب.")
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ حدث خطأ أثناء إرسال (circuits1.pdf): {e}")

        else:
            bot.send_message(chat_id, "📁 ملازم هذا المقرر قيد التجهيز وسيتم رفعها قريباً.")

    # 🖼️ صور وتسجيلات المحاضرات حسب المقرر المختار
    elif text == "🖼️ صور المحاضرات":
        current = user_course.get(chat_id)

        if current == "db":
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_lec2_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثانية (1)", url="https://drive.google.com/file/d/1CluNmUQBZHz8XIXE4LBwhwF-V7td7zsU/view?usp=drivesdk")
            btn_lec2_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثانية (2)", url="https://drive.google.com/file/d/1BOUOhEWM_58qwYdAwVEmlgbqR-UkQWBU/view?usp=drivesdk")
            btn_lec3 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثالثة", url="https://drive.google.com/file/d/1MWnbxfJ1uKWlcTJNjeqXoQ1RWaKcL7Qq/view?usp=drivesdk")
            btn_lec4 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الرابعة", url="https://drive.google.com/file/d/1WXykOVZT0iEIGHURpEqoWftjgwmrzojc/view?usp=drivesdk")
            btn_lec5 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الخامسة", url="https://drive.google.com/file/d/1NhlAoAXGAeYtpQXYLyfBSFOicLVyuxcq/view?usp=drivesdk")
            btn_lec6_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السادسة (1)", url="https://drive.google.com/file/d/1Jgmm7mreDcyga_2lgxyMlFcceFHh2ZP8/view?usp=drivesdk")
            btn_lec6_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السادسة (2)", url="https://drive.google.com/file/d/174Bu845BOF-EbUvGvuGG9WKAY4l1u_xK/view?usp=drivesdk")
            btn_lec7_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السابعة (1)", url="https://drive.google.com/file/d/1OlMW1vOoUdTV0Fnc2RkUEWKRUz6OujWx/view?usp=drivesdk")
            btn_lec7_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السابعة (2)", url="https://drive.google.com/file/d/1m4JzT_QKt8nrrsYNwc84gBX4aIvzhgC5/view?usp=drivesdk")
            markup.add(btn_lec2_p1, btn_lec2_p2, btn_lec3, btn_lec4, btn_lec5, btn_lec6_p1, btn_lec6_p2, btn_lec7_p1, btn_lec7_p2)
            bot.send_message(
                chat_id,
                "🖼️ تسجيلات ومحاضرات مقرر قواعد البيانات:",
                reply_markup=markup
            )

        elif current == "circuits":
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_c_lec2_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثانية (1)", url="https://drive.google.com/file/d/1mew2M-3lS0oLYcahdTroBYvo3_ThFlxe/view?usp=drivesdk")
            btn_c_lec2_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثانية (2)", url="https://drive.google.com/file/d/1STjTENZrOCgkP0LHPV4llDIJgGSDL-aI/view?usp=drivesdk")
            btn_c_lec3 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الثالثة", url="https://drive.google.com/file/d/1ZRP8crEXgCrVakvqVnCQuGo-xiwS5UY6/view?usp=drivesdk")
            btn_c_lec4_p1 = types.InlineKeyboardButton("🎥 رابط المحاضرة الرابعة (1)", url="https://drive.google.com/file/d/1H755EeI1zONyZBseEzEYVSEbS62_xn0k/view?usp=drivesdk")
            btn_c_lec4_p2 = types.InlineKeyboardButton("🎥 رابط المحاضرة الرابعة (2)", url="https://drive.google.com/file/d/1klBR708w14iagukT6DBIGXX8fWsnB8Ey/view?usp=drivesdk")
            btn_c_lec5_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الخامسة (1)", url="https://drive.google.com/file/d/1mvz3nReoe5GTU0noA9j_v-7mirTXZFTu/view?usp=drivesdk")
            btn_c_lec5_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة الخامسة (2)", url="https://drive.google.com/file/d/1qskIiBKI33crdzsxIwy7lzuucaa5oaYK/view?usp=drivesdk")
            btn_c_kirchhoff = types.InlineKeyboardButton("🎥 رابط تسجيل مراجعة قانون كيرشوف", url="https://drive.google.com/file/d/1-R1VjL-UGqR53SCHeML_r3TCdbX1yQH2/view?usp=drivesdk")
            btn_c_lec6_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السادسة (1)", url="https://drive.google.com/file/d/1h59EgfFlvXrfXTuDjKzAQVPFKRfFz74B/view?usp=drivesdk")
            btn_c_lec6_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السادسة (2)", url="https://drive.google.com/file/d/1h3U7DZD2EnztXolBhlBzwJI_ZLvZGazn/view?usp=drivesdk")
            btn_c_lec7_p1 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السابعة (1)", url="https://drive.google.com/file/d/1CBxdx6ZXYbxRFQOTuyB8NNzbsEpxUboo/view?usp=sharing")
            btn_c_lec7_p2 = types.InlineKeyboardButton("🎥 رابط تسجيل المحاضرة السابعة (2)", url="https://drive.google.com/file/d/1pJb2QsQPrxH_SfsI0O_rSh2rlipHSRex/view?usp=sharing")
            markup.add(
                btn_c_lec2_p1, btn_c_lec2_p2, btn_c_lec3,
                btn_c_lec4_p1, btn_c_lec4_p2,
                btn_c_lec5_p1, btn_c_lec5_p2,
                btn_c_kirchhoff,
                btn_c_lec6_p1, btn_c_lec6_p2,
                btn_c_lec7_p1, btn_c_lec7_p2
            )
            bot.send_message(
                chat_id,
                "🖼️ تسجيلات ومحاضرات مقرر مبادئ الدوائر الكهربائية:",
                reply_markup=markup
            )

        else:
            bot.send_message(chat_id, "🖼️ صور وتسجيلات هذا المقرر قيد التجهيز وسيتم رفعها قريباً.")

    elif text == "📝 ملخص المقرر" or text == "📋 نماذج اختبارات" or text == "⚙️ العملي":
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
        
