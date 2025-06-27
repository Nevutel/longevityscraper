from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>Anti-Aging Scraper</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Anti-Aging Research Scraper</h1>
            <p class="status">✅ Flask is working successfully!</p>
            <p>This is a test page to verify Flask is running properly.</p>
            <p>Next step: We'll add the full scraper functionality.</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("Starting Flask app...")
    print("Visit: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False) 