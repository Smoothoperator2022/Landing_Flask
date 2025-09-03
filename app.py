from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 🔑 Словник перекладів
translations = {
    "ru": {
        "title": "Финансово-аналитическая модель W.A. AI™",
        "subtitle": "Инструменты для анализа данных и стабильных решений",
        "intro": "Если вы выбрали нас, значит, вы ищете пассивный доход. Наша команда сотрудничает с разработчиками финансово-аналитической модели W.A. AI™, которая обеспечивает прозрачность и стабильность процессов. Вы можете проверить её работу в удобном режиме и оценить результат лично. При необходимости поддержку на каждом этапе готовы оказать консультанты.",
        "button1": "Запустить демонстрацию",
        "button2": "Запустить демонстрацию",
        "button3": "Запустить демонстрацию",
        "card1_title": "Моделирование данных",
        "card2_title": "Сценарная визуализация",
        "card3_title": "Гипотетическая модель",
        "section1_caption": "Мы используем AI для максимизации данных",
        "section2": "Инструмент интеллектуальной автоматизации действий с данными. Анализ. Визуализация. Прогнозирование на базе W.A. AI™",
        "section3": "Интегрировано в корпоративные процессы более 1500 команд. Это подтверждает ее надежность и технологическую устойчивость. Использование проверенных решений способствует стабильности и масштабируемости платформы.",
        "section4": "Наша платформа используется в цифровых процессах более 1500 команд. Это подтверждает ее надежность и технологическую устойчивость. Использование проверенных решений способствует стабильности и масштабируемости платформы.",
        "section5": "Система Scout™ для анализа сценариев. Вы можете в режиме реального времени отслеживать ключевые процессы и данные с помощью системы Scout™, которая обеспечивает высокую точность, надежность и прозрачность каждого этапа.",
        "analysis_title": "Аналитический вывод"
    },
    "en": {
        "title": "Financial-analytical model W.A. AI™",
        "subtitle": "Tools for data analysis and stable decisions",
        "intro": "By choosing us, you are looking for passive income. Our team works with developers of the financial-analytical model W.A. AI™, which ensures transparency and stability of processes. You can test its work in a convenient mode and evaluate the result personally. If necessary, support is provided at every stage.",
        "button1": "Start Demo",
        "button2": "Start Demo",
        "button3": "Start Demo",
        "card1_title": "Data Modeling",
        "card2_title": "Scenario Visualization",
        "card3_title": "Hypothetical Model",
        "section1_caption": "We use AI to maximize data",
        "section2": "A tool for intelligent automation of data operations. Analysis. Visualization. Forecasting based on W.A. AI™",
        "section3": "Integrated into corporate processes of more than 1500 teams. This confirms its reliability and technological sustainability. The use of proven solutions contributes to stability and scalability of the platform.",
        "section4": "Our platform is used in digital processes of more than 1500 teams. This confirms its reliability and technological sustainability. The use of proven solutions contributes to stability and scalability of the platform.",
        "section5": "Scout™ system for scenario analysis. You can track key processes and data in real time using Scout™, which provides high accuracy, reliability, and transparency at every stage.",
        "analysis_title": "Analytical Report"
    }
}

@app.route("/", methods=["GET", "POST"])
def index():
    lang = request.args.get("lang", "ru")  # за замовчуванням RU
    t = translations.get(lang, translations["ru"])

    if request.method == "POST":
        return redirect(url_for("form_page", lang=lang))

    return render_template("index.html", t=t, lang=lang)

@app.route("/form", methods=["GET", "POST"])
def form_page():
    lang = request.args.get("lang", "ru")
    return render_template("form.html", lang=lang)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")

    # Поки що просто виведемо в консоль (потім збережемо у файл/БД)
    print(f"Нова заявка: {name}, {phone}, {email}")

    return "Дякуємо, ваша заявка отримана!"

if __name__ == "__main__":
    app.run(debug=True)
