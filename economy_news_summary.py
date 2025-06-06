import os
import requests
from bs4 import BeautifulSoup
import feedparser
import openai


BBC_RSS = 'http://feeds.bbci.co.uk/news/business/economy/rss.xml'
REUTERS_RSS = 'http://feeds.reuters.com/news/economy'


class Article:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.text = None
        self.summary = None


def fetch_rss_entries(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append(Article(entry.title, entry.link))
    return articles


def fetch_article_text(article):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(article.link, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    article.text = '\n'.join(paragraphs)


def summarize(article, model='gpt-3.5-turbo'):
    if not article.text:
        return
    prompt = (
        "Summarize the following article about economy in a short paragraph:\n"
        f"{article.text[:4000]}"
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    article.summary = response["choices"][0]["message"]["content"].strip()


def main():
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    if not openai.api_key:
        raise EnvironmentError('OPENAI_API_KEY environment variable not set')

    sources = [BBC_RSS, REUTERS_RSS]
    articles = []
    for src in sources:
        articles.extend(fetch_rss_entries(src))

    for art in articles:
        fetch_article_text(art)
        summarize(art)
        print(f"Title: {art.title}\nLink: {art.link}\nSummary: {art.summary}\n")


if __name__ == '__main__':
    main()
