import asyncio
from aiosmtpd.controller import Controller
from email import message_from_bytes
from email.header import decode_header, make_header

class PrintHandler:
    async def handle_DATA(self, server, session, envelope):
        # перетворюємо байти на email.Message
        msg = message_from_bytes(envelope.content)

        # утиліта для декодування заголовків (Subject, From, To)
        def dec(header_value):
            if not header_value:
                return ""
            return str(make_header(decode_header(header_value)))

        subject = dec(msg.get("Subject"))
        sender = dec(msg.get("From"))
        to = dec(msg.get("To"))

        # тіло листа (беремо тільки text/plain)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = str(part.get("Content-Disposition"))
                if ctype == "text/plain" and "attachment" not in disp:
                    body = part.get_payload(decode=True).decode(
                        part.get_content_charset() or "utf-8",
                        errors="replace"
                    )
                    break
        else:
            body = msg.get_payload(decode=True).decode(
                msg.get_content_charset() or "utf-8",
                errors="replace"
            )

        # гарний вивід у консоль
        print("\n" + "=" * 60)
        print("✅ ОТРИМАНО ЛИСТ")
        print(f"From: {sender}")
        print(f"To:   {to}")
        print(f"Subj: {subject}")
        print("-" * 60)
        print(body.strip())
        print("=" * 60 + "\n")

        return "250 Message accepted for delivery"

if __name__ == "__main__":
    controller = Controller(PrintHandler(), hostname="localhost", port=1025)
    controller.start()
    print("🔌 Debug SMTP сервер слухає localhost:1025 (натисни Ctrl+C щоб зупинити)")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
        print("⏹ Зупинено")
