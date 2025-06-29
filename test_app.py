from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Anti-Aging Scraper Test</h1>
        <p>If you can see this, Flask is working!</p>
        <p>Status: ✅ Running successfully</p>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    print("Starting test Flask app...")
    print("Visit: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 