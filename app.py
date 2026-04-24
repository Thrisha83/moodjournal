from flask import Flask, render_template, request
from textblob import TextBlob
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, text TEXT, sentiment TEXT)")
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None

    if request.method == "POST":
        text = request.form["text"]

        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive 😊"
        elif polarity < 0:
            sentiment = "Negative 😔"
        else:
            sentiment = "Neutral 😐"

        conn = sqlite3.connect("database.db")
        conn.execute("INSERT INTO entries (text, sentiment) VALUES (?, ?)", (text, sentiment))
        conn.commit()
        conn.close()

    return render_template("index.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)