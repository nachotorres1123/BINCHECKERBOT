import logging
import json
import requests
from flask import Flask, request
import telegram
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler
import requests


app = Flask(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger()


class Config:
    TOKEN = "6466372597:AAGTPhW8XVaW64O_BDeY7k7Tq6yZXuacYZg"
    PORT = 5000


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Hola, ¿en qué puedo ayudarte?")


def check_bin(update, context):
    args = context.args
    if len(args) == 0:
        message = "ℹ️ Debes ingresar un número de BIN. Ejemplo: /check_bin 551238"
    elif len(args) != 1 or not args[0].isdigit() or len(args[0]) < 6:
        message = "❌ El formato del BIN ingresado es incorrecto. Debe tener al menos 6 dígitos."
    else:
        url = f"https://lookup.binlist.net/{args[0]}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "bank" in data:
                message = f"✅ Banco: {data['bank']['name']} ({data['bank']['url']})\n" \
                            f"✅ Tipo de tarjeta: {data['type']}\n" \
                            f"✅ País: {data['country']['name']}"
            else:
                message = "❌ No se encontró información para el BIN ingresado."
        else:
            message = "❌ No se pudo obtener información para el BIN ingresado. Inténtalo de nuevo más tarde."
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


bot = telegram.Bot(token=Config.TOKEN)

dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check_bin", check_bin))


@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"


def main():
    config = Config()
    app.run(host="0.0.0.0", port=config.PORT)


if __name__ == "__main__":
    main()
