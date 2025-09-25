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
        "title_form":"Встречайте W.A. AI™",
        "subtitle": "Инструменты для анализа данных и стабильных решений",
        "subtitle_form":"Зарабатывайте от 10 000€ в месяц при минимальном вкладе в 250€ ,благодаря доступу к нашей платформ!",
        "text1": """Если вы выбрали нас, значит, вы ищете стабильные решения для дохода 
            без постоянного участия. Наша команда сотрудничает с разработчиками 
            финансово-аналитической модели W.A. AI™, которая обеспечивает прозрачность 
            и стабильность процессов. Вы можете проверить её работу в удобном режиме 
            и оценить результат лично. При необходимости наши консультанты готовы 
            оказать поддержку на каждом этапе.""",
        "text2": "Инструмент интеллектуальной автоматизации действий с данными. Анализ. Визуализация. Прогнозирование — на базе W.A. AI™",
        "text3": "Интегрировано в корпоративные процессы более 1500 команд",
        "text4": """Наша платформа используется в цифровых процессах более 1500 команд.
                    Это подтверждает ее надежность и технологическую устойчивость.
                    Использование проверенных решений способствует стабильности и масштабируемости платформы.""",
        "scout": """Система Scout™ для анализа сценариев
                    Вы можете в режиме реального времени отслеживать ключевые
                    процессы и данные с помощью системы Scout™, которая обеспечивает высокую
                    точность, надежность и прозрачность каждого этапа""",
        "title_company": "W.A. AI™",
        "company_contact":"""Company Name: Voss Digital Solutions. Managing Director: Daniel Voss. Address: Musterstrasse 12, 10115 Berlin, Germany.
        Contact:Phone: +49 (0)30 1234567, e-mail: info@vistaquant.net. Responsible for content (according to § 55 Abs. 2 RStV): Daniel Voss, address as above""",
        "impressum":"""The contents of this website were created with great care. However, we cannot guarantee the accuracy, completeness or timeliness of the information provided. As a service provider, we are responsible for our own content on
        these pages in accordance with general laws. We are not obligated to monitor transmitted or stored third-party information or to investigate circumstances that indicate illegal activity. Liability for links: Our offer contains links
        to external websites of third parties, on whose contents we have no influence. Therefore, we cannot assume any liability for these external contents. The respective provider or operator of the pages is always responsible for the
        content of the linked pages. Furthermore, this website does not provide financial or investment advice. Any information is for demonstration purposes only and must not be relied upon as a basis for financial decisions.""",
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
        "title_form": "Meet W.A. AI™",
        "subtitle": "Tools for data analysis and stable solutions",
        "subtitle_form": "Earn from €10,000 per month with a minimum deposit of €250 by accessing our platform!",
        "text1": """If you have chosen us, it means you are looking for stable income 
            solutions without constant involvement. Our team works with the developers 
            of the W.A. AI™ financial analysis model, which ensures transparency 
            and stability of processes. You can check how it works at your convenience 
            and evaluate the results yourself. If necessary, our consultants are 
            ready to provide support at every stage.""",
        "text2": "An intelligent tool for automating data operations. Analysis. Visualization. Forecasting — powered by W.A. AI™",
        "text3": "Integrated into corporate processes of more than 1500 teams",
        "text4": """Our platform is already used in the digital workflows of more than 1500 teams. 
                    This proves its reliability and technological resilience. 
                    Using trusted solutions contributes to the platform’s stability and scalability.""",
        "scout": """The Scout™ system for scenario analysis. 
                    You can track key processes and data in real time with Scout™, 
                    which ensures high accuracy, reliability, and transparency at every stage.""",
        "title_company": "W.A. AI™",
        "company_contact": """Company Name: Voss Digital Solutions. Managing Director: Daniel Voss. Address: Musterstrasse 12, 10115 Berlin, Germany.
        Contact: Phone: +49 (0)30 1234567, e-mail: info@vistaquant.net. Responsible for content (according to § 55 Abs. 2 RStV): Daniel Voss, address as above""",
        "impressum": """The contents of this website were created with great care. However, we cannot guarantee the accuracy, completeness or timeliness of the information provided...
        (залишаємо як у тебе, англійський текст був правильний)""",
        "button1": "Start Demo",
        "button2": "Learn More",
        "button3": "Check the Model",
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
        bg = url_for("static", filename="img/Land_page_1_en_notext.png")
    else:
        bg = url_for("static", filename="img/Land_page_1_ru_notext.png")

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
        bg = url_for("static", filename="img/Land_page_2_en_notext.png")
    else:
        bg = url_for("static", filename="img/Land_page_2_ru_notext.png")

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

