from flask import Flask, render_template, request

app = Flask(__name__)

# --- Переклади ---
translations = {
    "ru": {
        "title": "Финансово-аналитическая модель W.A. AI™",
        "title_form":"Встречайте W.A. AI™",
        "subtitle": "Инструменты для анализа данных и стабильных решений",
        "subtitle_form":"Зарабатывайте от 10 000€ в месяц при минимальном вкладе в 250€ ,благодаря доступу к нашей платформ!",
        "text1": """Вы брали нас, а значит Вы ищете стабильные решения для дохода без постоянного участия.
         Финансово-аналитическая модель W.A. AI™ объединяет в себе инструменты для глубокого анализа данных и выработки решений,
          которые можно применять в долгосрочной перспективе.
            Мы делаем акцент на прозрачности процессов, чтобы у вас была возможность самостоятельно проверить результат и убедиться в его устойчивости.
            Наша команда сопровождает пользователей на всех этапах работы: от базовой настройки до комплексных сценариев анализа.
            Система построена таким образом, что даже при минимальном участии с вашей стороны результаты будут доступны в удобной и понятной форме.""",

        "card1_title": "Моделирование данных",
        "card1_value": "25 050",
        "card1_meta": "Доход 1 400 • Расход 40.00",

        "card2_title": "Сценарная визуализация",
        "card2_value": "21 054",
        "card2_meta": "Метод оплаты +12%",

        "card3_title": "Гипотетическая модель",
        "card3_value": "120 /year",
        "card3_meta": "5 Пользователей • Поддержка",

        "card4_title": "Аналитический вывод",
        "card4_value": "25 050",
        "card4_meta": "Income 1 400.24 • Expenses 40.00",

        "anal_title": "Аналитический вывод",
        "anal_value": "25,050",

        "text2": """Инструмент интеллектуальной автоматизации W.A. AI™ работает как универсальный помощник в работе с данными.
         С его помощью можно автоматизировать рутинные действия, визуализировать сложные процессы и строить прогнозы на основе накопленной информации.
        Такая интеграция облегчает работу с большими массивами данных, позволяя компаниям принимать решения быстрее и точнее.
        Система создавалась в сотрудничестве с экспертами из разных сфер, что обеспечивает её универсальность:
        она одинаково хорошо подходит и для финансового анализа, и для бизнес-планирования, и для оценки операционных процессов.""",
        "text3": "Интегрировано в корпоративные процессы более 1500 команд",
        "text4": """Сегодня W.A. AI™ интегрирована в рабочие процессы более чем 1500 команд, что подтверждает её практическую ценность и надежность.
                    Технологическая основа платформы строится на проверенных решениях, которые проходят регулярное обновление и адаптацию под современные задачи.
                    Это обеспечивает устойчивость системы даже при высоких нагрузках и позволяет масштабировать её для компаний любого размера.
                    Использование платформы упрощает ежедневную работу и делает её более предсказуемой, что особенно важно в условиях постоянно меняющейся бизнес-среды.""",
        "scout": """Scout™ — это модуль внутри W.A. AI™, который отвечает за анализ сценариев и отслеживание процессов в режиме реального времени.
                    Система позволяет быстро выявлять изменения в ключевых параметрах, что повышает точность и сокращает время на проверку данных.
                    Scout™ создана для того, чтобы бизнес мог принимать решения без задержек, опираясь на актуальную информацию.
                    Прозрачность каждого этапа помогает минимизировать риски и повышает доверие к результатам.""",


        "title_company": "W.A. AI™",
        "company_contact":"""Company Name: Voss Digital Solutions. Managing Director: Daniel Voss. Address: Musterstrasse 12, 10115 Berlin, Germany.
        Contact:Phone: +49 (0)30 5729641, e-mail: info@vistaquant.net. Responsible for content (according to § 55 Abs. 2 RStV): Daniel Voss, address as above""",
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
        "text1": """You chose us, which means you are looking for stable income solutions without constant involvement.
         The W.A. AI™ financial analysis model combines tools for in-depth data analysis and decision-making that can be applied in the long term.
        We emphasize transparency in our processes so that you can independently verify the results and ensure their sustainability.
        Our team supports users at all stages of the process, from basic configuration to complex analysis scenarios.
        The system is designed so that even with minimal involvement on your part, the results will be available in a convenient and understandable form.""",

        "card1_title": "Data Modeling",
        "card1_value": "25,050",
        "card1_meta": "Income 1,400 • Expenses 40.00",

        "card2_title": "Scenario Visualization",
        "card2_value": "21,054",
        "card2_meta": "Payment Method +12%",

        "card3_title": "Hypothetical Model",
        "card3_value": "120 /year",
        "card3_meta": "5 Users • Support",

        "card4_title": "Analytical Output",
        "card4_value": "25,050",
        "card4_meta": "Income 1,400.24 • Expenses 40.00",


        "anal_title": "Analytical Report",
        "anal_value": "25,050",

        "text2": """The W.A. AI™ intelligent automation tool works as a universal assistant for working with data.
         It can be used to automate routine tasks, visualize complex processes, and make predictions based on accumulated information.
        This integration facilitates working with large data sets, allowing companies to make decisions faster and more accurately.
        The system was developed in collaboration with experts from various fields, ensuring its versatility:
        it is equally well suited for financial analysis, business planning, and operational process evaluation.""",
        "text3": "Integrated into corporate processes of more than 1500 teams",
        "text4": """Today, W.A. AI™ is integrated into the workflows of more than 1,500 teams, confirming its practical value and reliability.
                    The platform's technological foundation is built on proven solutions that are regularly updated and adapted to modern tasks.
                    This ensures the stability of the system even under high loads and allows it to be scaled for companies of any size.
                    Using the platform simplifies daily work and makes it more predictable, which is especially important in an ever-changing business environment.""",
        "scout": """Scout™ is a module within W.A. AI™ that is responsible for analyzing scenarios and tracking processes in real time.
                    The system allows you to quickly identify changes in key parameters, which increases accuracy and reduces the time spent on data verification.
                    Scout™ is designed to enable businesses to make decisions without delay, based on up-to-date information.
                    Transparency at every stage helps minimize risks and increases confidence in the results.""",
        "title_company": "W.A. AI™",
        "company_contact":"""Company Name: Voss Digital Solutions. Managing Director: Daniel Voss. Address: Musterstrasse 12, 10115 Berlin, Germany.
        Contact:Phone: +49 (0)30 5729641, e-mail: info@vistaquant.net. Responsible for content (according to § 55 Abs. 2 RStV): Daniel Voss, address as above""",
        "impressum":"""The contents of this website were created with great care. However, we cannot guarantee the accuracy, completeness or timeliness of the information provided. As a service provider, we are responsible for our own content on
        these pages in accordance with general laws. We are not obligated to monitor transmitted or stored third-party information or to investigate circumstances that indicate illegal activity. Liability for links: Our offer contains links
        to external websites of third parties, on whose contents we have no influence. Therefore, we cannot assume any liability for these external contents. The respective provider or operator of the pages is always responsible for the
        content of the linked pages. Furthermore, this website does not provide financial or investment advice. Any information is for demonstration purposes only and must not be relied upon as a basis for financial decisions.""",
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

@app.route("/")
def index():
    lang = request.args.get("lang", "ru")  # по замовчуванню російська
    t = translations.get(lang, translations["ru"])
    return render_template("index.html", t=t, lang=lang)

if __name__ == "__main__":
    app.run(debug=True)
