# Reddit Trend Miner

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Scrapy](https://img.shields.io/badge/scrapy-2.11-green.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.7-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

Data mining application that scrapes Reddit at scale, parses post metadata via XPath and JSON, and generates word-frequency histograms per subreddit using Matplotlib. Built with Scrapy, Beautiful Soup, and Selenium WebDriver. Statistical analysis layer written in R.

## Pipeline

```
https://reddit.com/r/{sub}/top.json
          |
     Scrapy Spider
     (JSON parsing + XPath extraction)
          |
     Item Pipeline
      /          \
CSV export    Matplotlib
              output/word_freq_{sub}.png
```

## Tech Stack

| Tool | Role |
|---|---|
| Scrapy | Spider framework, request scheduling, item pipeline |
| Beautiful Soup | HTML DOM parsing and text extraction |
| Selenium WebDriver | Dynamic page interaction and JS-rendered content |
| XPath | DOM property targeting |
| Matplotlib | Word frequency histograms |
| R | Statistical distribution analysis |

## Setup

```bash
pip install -r requirements.txt
mkdir output
```

## Usage

```bash
cd RedditScraper
scrapy crawl reddit -o ../output/posts.csv
```

Outputs:
- `output/posts.csv` — title, score, comment count, url, created timestamp, subreddit
- `output/word_freq_{subreddit}.png` — top-30 word frequency histogram

## Configuration

Edit `subreddits` in `RedditScraper/RedditScraper/spiders/parse.py` to target different communities:

```python
subreddits = ['ucsd', 'datascience', 'Python']
```

## Sample Output

```
frequency
   |
15 |  ##
12 |  ##  ##
 9 |  ##  ##  ##
 6 |  ##  ##  ##  ##
 3 |  ##  ##  ##  ##  ##
   +-----------------------------> words
      ucsd gpa finals exam week
```

## Context

Started as a data mining project at UC San Diego. The scraping and data pipeline patterns from this project carried into ETL work at Teradata and CI artifact ingestion and log parsing at Qualcomm (475+ Jenkins pipelines across 10 product lines, 5 global regions).
