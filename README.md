# Anti-Aging Research Webscraper

An automated web scraper that fetches the latest anti-aging research articles from leading medical and scientific websites, with a beautiful web dashboard.

## Features

- **Automated Scraping**: Runs daily at 7:00 AM automatically
- **Real-time Dashboard**: Beautiful web interface to view articles
- **Smart Filtering**: Only captures articles related to anti-aging, longevity, and senescence
- **AI Summarization**: Uses OpenAI to generate concise summaries (optional)
- **Multiple Sources**: Scrapes 12+ leading medical and scientific websites
- **API Endpoints**: RESTful API for programmatic access

## Target Websites

- Medical News Today
- JAMA Network
- Science Daily
- Cell
- Nature
- ScienceDirect
- News Medical
- Yale Medicine
- Nature Aging
- Wiley Aging Cell
- SciTech Daily
- Science Alert

## Keywords Filtered

- anti-aging
- longevity
- senescence
- aging
- gerontology
- telomere
- sirtuin
- rapamycin
- metformin
- NAD+
- mitochondria
- autophagy
- inflammation
- oxidative stress
- cellular aging
- biological age
- epigenetic clock
- senolytics

## Local Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (optional, for summaries)

### Installation

1. **Clone or download the project**
2. **Navigate to the project directory**
   ```bash
   cd CursorCode
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set OpenAI API key (optional)**
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-openai-api-key"
   
   # Mac/Linux
   export OPENAI_API_KEY="your-openai-api-key"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   - Go to [http://localhost:5000](http://localhost:5000)
   - You'll see the dashboard with controls and article display

## Deployment

### Option 1: Render (Recommended - Free Tier)

1. **Push your code to GitHub**

2. **Go to [Render.com](https://render.com/)**
   - Sign up with your GitHub account
   - Click "New +" → "Web Service"

3. **Connect your repository**
   - Select your GitHub repo
   - Give your service a name

4. **Configure the service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Environment**: Python 3

5. **Add environment variables**
   - Click "Environment" tab
   - Add: `OPENAI_API_KEY` = your-api-key

6. **Deploy**
   - Click "Create Web Service"
   - Your app will be live at `https://your-app-name.onrender.com`

### Option 2: Railway

1. **Push your code to GitHub**

2. **Go to [Railway.app](https://railway.app/)**
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"

3. **Select your repository**

4. **Add environment variables**
   - Click "Variables" tab
   - Add: `OPENAI_API_KEY` = your-api-key

5. **Deploy**
   - Railway will automatically detect it's a Python app
   - Your app will be live at the provided URL

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

4. **Set environment variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

## Usage

### Dashboard Features

1. **View Articles**: All scraped articles are displayed with titles, summaries, and source information
2. **Manual Scraping**: Click "Start Scraping" to trigger immediate scraping
3. **Real-time Status**: See if scraping is running, last run time, and article count
4. **Article Links**: Click on any article to read the full content on the original website

### API Endpoints

- `GET /` - Main dashboard
- `GET /api/status` - Get scraping status
- `GET /api/articles` - Get all articles as JSON
- `POST /api/scrape` - Trigger manual scraping

### Automation

- The scraper runs automatically every day at 7:00 AM (server time)
- No manual intervention required
- Results are saved to CSV files and displayed on the dashboard

## Configuration

Edit `config.py` to:
- Add/remove target websites
- Modify keywords for filtering
- Adjust scraping settings
- Change output file names

## Troubleshooting

### Common Issues

1. **"No articles found"**
   - Check if target websites are accessible
   - Verify keywords in config.py
   - Check scraper.log for errors

2. **OpenAI API errors**
   - Verify your API key is correct
   - Check your OpenAI account has credits
   - The scraper will work without OpenAI (no summaries)

3. **Deployment issues**
   - Ensure all files are committed to Git
   - Check environment variables are set correctly
   - Verify requirements.txt includes all dependencies

### Logs

- Check `scraper.log` for detailed scraping information
- Deployment platforms have their own log systems

## File Structure

```
CursorCode/
├── app.py                 # Flask web application
├── scraper.py            # Main scraping logic
├── summarizer.py         # OpenAI summarization
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── templates/
│   └── dashboard.html    # Web dashboard template
├── venv/                # Virtual environment
└── README.md            # This file
```

## Contributing

Feel free to:
- Add new target websites
- Improve the filtering algorithm
- Enhance the dashboard design
- Add new features

## License

MIT License - feel free to use and modify as needed. 