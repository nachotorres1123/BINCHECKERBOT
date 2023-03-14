import logging
import json
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, CommandHandler
import requests

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hola, ¿en qué puedo ayudarte?")

def check_bin(update, context):
    args = context.args
    if len(args) == 0:
        message = "❌ Debes proporcionar un número de BIN."
    else:
        bin_number = args[0]
        url = f"https://lookup.binlist.net/{bin_number}"
        response = requests.get(url)
        data = json.loads(response.text)
        if "valid" in data and data["valid"]:
            card = data["card"]
            issuer = data["issuer"]
            country = data["country"]
            message = "✅Coco valido.\n"
            message += f"Esquema: {card['scheme']}\n"
            message += f"Tipo: {card['type']}\n"
            message += f"Categoria: {card['category']}\n"
            message += f"Emisor: {issuer['name']}\n"
            message += f"URL: {issuer['url']}\n"
            message += f"Telefono: {issuer['tel']}\n"
            message += f"País: {country['name']}\n"
            message += f"Codigo Numerico: {country['numeric code']}\n"
            message += f"Codigo Alpha 2: {country['alpha 2 code']}\n"
            message += f"Latitud: {country['latitude']}\n"
            message += f"Longitud: {country['longitude']}\n"
            message += f"Moneda: {country['currency']}\n"
            message += f"Nombre Moneda: {country['currency name']}\n"
        else:
            message = "❌ El BIN ingresado no es válido."
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

dispatcher = Dispatcher(bot=None, update_queue=None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check_bin", check_bin))

@app.route("/", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

def main():
    config = Config()
    global bot
    bot = telegram.Bot(config.TOKEN)
    dispatcher.bot = bot
    app.run(host="0.0.0.0", port=config.PORT)

if __name__ == "__main__":
    main()