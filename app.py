from flask import Flask, render_template, request, redirect, url_for, session

import smtplib, os
from email.mime.text import MIMEText
from dotenv import load_dotenv


# завантажуємо змінні з .env
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"  # щоб працювала session

# Налаштування SMTP (Hostinger)
# SMTP_HOST = os.getenv("SMTP_HOST")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASS = os.getenv("SMTP_PASS")
# RECIPIENTS = os.getenv("RECIPIENTS", SMTP_USER).split(",")

SMTP_HOST = os.getenv("MAIL_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("MAIL_PORT", 465))
SMTP_USER = os.getenv("MAIL_USER", "info@vistaquant.net")
SMTP_PASS = os.getenv("MAIL_PASS", "secret")
# RECIPIENTS = os.getenv("RECIPIENTS", SMTP_USER).split(",")
RECIPIENTS = [addr.strip() for addr in os.getenv("RECIPIENTS", SMTP_USER).split(",")]

# --- Переклади ---
translations = {
    "ru": {
        "title": "Финансово-аналитическая модель W.A. AI™",
        "subtitle": "Инструменты для анализа данных и стабильных решений",
        "button1": "Запустить демонстрацию",
        "button2": "Узнать подробности",
        "button3": "Проверить работу модели",
        "form_title": "Пожалуйста, введите Ваши данные, чтобы получить доступ к демонстрации",
        "form_name": "Имя",
        "form_phone": "Телефон",
        "form_email": "Email",
        "form_submit": "Отправить",
        "form_success": "Спасибо, Ваши данные не передаются третьим лицам, наши сотрудники свяжутся с Вами в ближайшее время"
    },
    "en": {
        "title": "W.A. AI™ Financial Analysis Model",
        "subtitle": "Tools for data analysis and stable solutions",
        "button1": "Start Demo",
        "button2": "Learn more",
        "button3": "Check the model's performance",
        "form_title": "Please, enter your data to get access to the demo",
        "form_name": "Name",
        "form_phone": "Phone",
        "form_email": "Email",
        "form_submit": "Send",
        "form_success": "Thank you! Your data is not shared with third parties. Our team will contact you shortly."
    }
}

# ---------- ГОЛОВНА ----------
@app.route("/")
def index():
    lang = request.args.get("lang", "ru")
    t = translations.get(lang, translations["ru"])

    if lang == "en":
        bg = url_for("static", filename="img/Land_page_1_en.png")
    else:
        bg = url_for("static", filename="img/Land_page_1_ru.png")

    return render_template("index.html", bg=bg, lang=lang, t=t)

# ---------- Надсилання листа через Mailtrap ----------
def send_email(name, phone, email):
    msg = MIMEText(f"Имя: {name}\nТелефон: {phone}\nEmail: {email}")
    msg["Subject"] = "Новая заявка с лендинга"
    msg["From"] = SMTP_USER
    msg["To"] = ", ".join(RECIPIENTS)   # рядок для заголовка


    # Якщо порт 1025 → тестовий режим
    if SMTP_PORT == 1025:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.sendmail(SMTP_USER, RECIPIENTS, msg.as_string())
            print("✅ Тестовий лист відправлено (дивись у терміналі з smtpd)")
    else: # реальний SMTP Hostinger
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, RECIPIENTS, msg.as_string())
            print("✅ Реальний лист відправлено")

    # try:
    #     # Візьми логін/пароль із Mailtrap (Sandbox → Inboxes → SMTP settings)
    #     with smtplib.SMTP("sandbox", 245345) as server:
    #         # Для Mailtrap `starttls()` не обов’язковий, але не завадить
    #         # server.starttls()
    #         server.login("")
    #         server.send_message(msg)
    #         print("✅ Лист отправлен в Mailtrap")
    # except Exception as e:
    #     print("❌ Ошибка отправки:", e)

# ---------- СТОРІНКА ФОРМИ ----------
@app.route("/form", methods=["GET", "POST"])
def form():
    lang = request.args.get("lang", "ru")
    t = translations.get(lang, translations["ru"])

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        # Надсилаємо лист у Mailtrap
        send_email(name, phone, email)

        session["submitted"] = True
        return redirect(url_for("form", lang=lang))

    # фон другої сторінки
    if lang == "en":
        bg = url_for("static", filename="img/Land_page_2_en.png")
    else:
        bg = url_for("static", filename="img/Land_page_2_ru.png")

    submitted = session.get("submitted", False)
    return render_template("form.html", bg=bg, submitted=submitted, lang=lang, t=t)

# утиліта, щоб почистити прапорець і знову побачити форму
@app.route("/form/reset")
def form_reset():
    session.pop("submitted", None)
    lang = request.args.get("lang", "ru")
    return redirect(url_for("form", lang=lang))

if __name__ == "__main__":
    app.run(debug=True)

