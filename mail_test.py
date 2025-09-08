import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.hostinger.com"   # Hostinger SMTP сервер
SMTP_PORT = 465                     # порт
SMTP_USER = "info@vistaquant.net"   # твоя корпоративна пошта
SMTP_PASS = "QuazDojo-2025"         # пароль від пошти (Hostinger дає в hPanel)

def send_email(name, phone, email):
    msg = MIMEText(f"Имя: {name}\nТелефон: {phone}\nEmail: {email}")
    msg["Subject"] = "Новая заявка с формы"
    msg["From"] = SMTP_USER
    msg["To"] = "info@vistaquant.net, testmail@gmail.com"  # для перевірки

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server: # with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        # server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    send_email("Тест", "+380991112233", "test@example.com")
    print("✅ Тестовый email отправлен")
