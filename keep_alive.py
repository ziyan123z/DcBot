from flask import Flask
from threading import Thread
import requests
import time

app = Flask('')


@app.route('/')
def home():
    return "✅ Bot aktif!"


def ping_self():
    while True:
        try:
            requests.get("https://replit.com/@ziyan310711/BotDc/main.py")
        except:
            pass
        time.sleep(10)


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t1 = Thread(target=run)
    t2 = Thread(target=ping_self)
    t1.start()
    t2.start()
