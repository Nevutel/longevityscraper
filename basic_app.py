from flask import Flask; app = Flask(__name__); @app.route("/"); def hello(): return "Anti-Aging Scraper is working!"; print("Starting Flask..."); app.run(host="127.0.0.1", port=5000)
