import os
import json
from flask import Flask, request, redirect, render_template
import random
import string
from urllib.parse import urlparse

app = Flask(__name__)

DB_FILE = "database.json"

# Load database from file
def load_db():
    if not os.path.exists(DB_FILE):
        return {"short_to_long": {}, "long_to_short": {}}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Save database to file
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Short code generation
def generate_short_code(length=3):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_short_keyword(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")
    if "facebook" in domain:
        return "fb"
    elif "youtube" in domain:
        return "yt"
    elif "google" in domain:
        return "gg"
    elif "twitter" in domain:
        return "tw"
    elif "linkedin" in domain:
        return "li"
    elif "instagram" in domain:
        return "ig"
    else:
        return domain[:2]

@app.route('/', methods=['GET', 'POST'])
def index():
    db = load_db()
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        if long_url in db['long_to_short']:
            code = db['long_to_short'][long_url]
        else:
            keyword = get_short_keyword(long_url)
            while True:
                code = keyword + generate_short_code()
                if code not in db['short_to_long']:
                    break
            db['short_to_long'][code] = long_url
            db['long_to_short'][long_url] = code
            save_db(db)
        short_url = request.host_url + code
    return render_template('index.html', short_url=short_url)

@app.route('/<code>')
def redirect_to_long_url(code):
    db = load_db()
    long_url = db['short_to_long'].get(code)
    if long_url:
        return redirect(long_url)
    return "❌ Short URL not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
