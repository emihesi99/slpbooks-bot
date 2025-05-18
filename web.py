from flask import Flask
from threading import Thread
import os  # اینو اضافه کن

app = Flask('')

@app.route('/')
def home():
    return "ربات گفتاردرمانی امیر جون فعاله!"

def run():
    port = int(os.environ.get("PORT", 8080))  # این خط مهمه
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
