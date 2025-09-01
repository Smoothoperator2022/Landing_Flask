import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_mail import Mail, Message
from dotenv import load_dotenv

import time
import uuid
from urllib.parse import urlparse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask_wtf.csrf import CSRFProtect
from flask import (
    Flask, render_template, redirect, url_for, flash, request,
    session, make_response, abort
)

# Завантажимо .env якщо є
load_dotenv()

app = Flask(__name__)

# Базові налаштування
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

# Налаштування пошти
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '1025'))
app.config['MAIL_USE_TLS'] = bool(int(os.getenv('MAIL_USE_TLS', '0')))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'no-reply@example.com')

# Одержувачі (дві адреси через кому в .env)
recipients_env = os.getenv('RECIPIENTS', '')
RECIPIENTS = [addr.strip() for addr in recipients_env.split(',') if addr.strip()]

mail = Mail(app)

# --- Форма ---
class DemoForm(FlaskForm):
    name = StringField("Ім'я", validators=[
        DataRequired(message="Вкажіть ім'я"),
        Length(max=100)
    ])
    phone = StringField("Телефон", validators=[
        DataRequired(message="Вкажіть телефон"),
        Length(max=30)
    ])
    email = StringField("Електронна пошта", validators=[
        DataRequired(message="Вкажіть email"),
        Email(message="Невірний формат email"),
        Length(max=254)
    ])
    submit = SubmitField("Надіслати")

# --- Маршрути ---


# Увімкнути CSRF глобально
CSRFProtect(app)

# Сигнер для коротких маркерів (підписаний токен у cookie — опціонально)
signer = URLSafeTimedSerializer(app.config['SECRET_KEY'], salt="gate-token")

# Хелпер: чи наш реферер з того самого домену
def _same_origin(req: request) -> bool:
    ref = req.referrer
    if not ref:
        return False
    ref_host = urlparse(ref).netloc
    return ref_host == req.host

# Хелпер: простий фільтр підозрілих ботів (додатковий, не обов'язковий)
BAD_BOTS = (
    "adsbot-google", "googlebot", "mediapartners-google",
    "facebookexternalhit", "facebot", "bingbot", "yandexbot",
    "bot", "crawler", "spider", "preview", "linkchecker"
)
def _looks_like_bot(req: request) -> bool:
    ua = (req.headers.get("User-Agent") or "").lower()
    return any(k in ua for k in BAD_BOTS)

# ---------- A: головна (кнопка без href) ----------
@app.get("/")
def index():
    # рендериш як і раніше (кнопка всередині <form method="POST" action="/go">)
    return render_template("index.html")

# ---------- GATE: приймає тільки POST ----------
@app.post("/go")
def go():
    # 1) базові перевірки
    if not _same_origin(request):
        abort(400)  # чужий реферер — ні
    if _looks_like_bot(request):
        return ("", 204)  # для ботів — нічого (опційно)

    # 2) короткоживучий маркер у сесії (одноразовий)
    session["gate_ts"] = time.time()
    session["gate_nonce"] = uuid.uuid4().hex  # щоб не повторювалися
    session.modified = True

    # 3) (опціонально) продублюємо маркером у cookie з підписом
    token = signer.dumps({"n": session["gate_nonce"]})
    resp = redirect(url_for("start"), code=303)  # 303 See Other → /start
    resp.set_cookie(
        "gate_token", token,
        max_age=5 * 60, secure=False, httponly=True, samesite="Lax"
    )
    return resp

# ---------- B: захищена сторінка ----------
@app.get("/start")
def start():
    # 1) перевіряємо сесію
    ts = session.pop("gate_ts", None)   # pop → одноразово
    nonce = session.pop("gate_nonce", None)
    if not ts or not nonce or (time.time() - ts) > 5 * 60:
        # запізно або прямий перехід: назад на /demo (або на /)
        return redirect(url_for("demo"))

    # 2) (опціонально) звіряємо підписаний cookie
    token = request.cookies.get("gate_token")
    try:
        data = signer.loads(token, max_age=5 * 60)
        if data.get("n") != nonce:
            return redirect(url_for("demo"))
    except (BadSignature, SignatureExpired, TypeError):
        return redirect(url_for("demo"))

    # 3) рендер сторінки B + noindex/nofollow + no-store
    resp = make_response(render_template("start.html"))
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    # Мету з noindex додамо прямо у шаблон (див. нижче)
    return resp

# ---------- demo як і був ----------
# @app.route("/demo", methods=["GET", "POST"])
# def demo(): ...


@app.route("/demo", methods=["GET", "POST"])
def demo():
    form = DemoForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        phone = form.phone.data.strip()
        email = form.email.data.strip()

        subject = "Запит на демонстрацію (лендинг)"
        body = (
            f"Ім'я: {name}\n"
            f"Телефон: {phone}\n"
            f"E-mail: {email}\n"
            f"Джерело: {request.url_root}"
        )

        # Якщо RECIPIENTS не задані — зупиняємо з помилкою конфігурації
        if not RECIPIENTS:
            flash("Помилка конфігурації: не вказані адреси одержувачів (RECIPIENTS).", "error")
            return redirect(url_for("demo"))

        try:
            msg = Message(subject=subject, body=body, recipients=RECIPIENTS, reply_to=email)
            mail.send(msg)
            flash("Дякуємо! Заявку надіслано.", "success")
            return redirect(url_for("demo"))
        except Exception as e:
            # Лог і контрольоване повідомлення
            app.logger.exception("Помилка відправки пошти")
            flash(f"Помилка відправки пошти: {e}", "error")
            return redirect(url_for("demo"))

    return render_template("demo.html", form=form)



if __name__ == "__main__":
    # Запуск: python app.py
    app.run(host="0.0.0.0", port=5000, debug=bool(int(os.getenv('FLASK_DEBUG', '1'))))
