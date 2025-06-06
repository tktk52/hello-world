# Economy News Summarizer

This repository contains a simple Python script that fetches economy related
articles from BBC and Reuters RSS feeds and summarizes each article using the
OpenAI API.

## Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`
- `feedparser`
- `openai`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

Set your OpenAI API key in the environment variable `OPENAI_API_KEY` and run:

```bash
python economy_news_summary.py
```

The script will print the title, link and summary for each economy article found
in the feeds.
