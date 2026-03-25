import sqlite3
import threading
import time

import mss
from flask import Flask, render_template

import config
from collector.ocr_engine import image_to_text
from collector.screen_reader import capture_zone
from database.models import init_db, save_price

app = Flask(__name__)
init_db()


def background_collector():
    """Boucle infinie qui scanne l'ecran en arriere-plan."""
    with mss.mss() as sct:
        while True:
            # 1. Capture RAM
            img_nom = capture_zone(sct, config.ZONE_NOM)
            img_prix = capture_zone(sct, config.ZONE_PRIX)

            # 2. OCR
            name = image_to_text(img_nom)
            price_str = image_to_text(img_prix, is_price=True)

            # 3. Validation et sauvegarde
            if name and price_str.isdigit():
                save_price(name, int(price_str))
                print(f"[{name}] enregistre a {price_str}k")

            time.sleep(config.SCAN_INTERVAL)


# Lancer le collector dans un thread separe
threading.Thread(target=background_collector, daemon=True).start()


@app.route("/")
def index():
    # Recuperer les 20 derniers prix pour le dashboard
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, date FROM prices ORDER BY date DESC LIMIT 20")
    recent_data = cursor.fetchall()
    conn.close()
    return render_template("index.html", data=recent_data)


if __name__ == "__main__":
    app.run(port=5000)
