from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working on Vercel!"

@app.route("/test")
def test():
    return jsonify({"status": "success", "message": "Test endpoint works!"})

if __name__ == "__main__":
    app.run()
