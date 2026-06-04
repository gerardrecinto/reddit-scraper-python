import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

import scrapy
from RedditScraper.items import RedditscraperItem


class RedditSpider(scrapy.Spider):
    name = "reddit"
    custom_settings = {
        'USER_AGENT': 'reddit-trend-miner/1.0',
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': False,
    }

    subreddits = ['ucsd', 'datascience', 'Python']

    def start_requests(self):
        for sub in self.subreddits:
            yield scrapy.Request(
                f'https://www.reddit.com/r/{sub}/top.json?limit=100&t=week',
                callback=self.parse,
                cb_kwargs={'subreddit': sub},
                headers={'Accept': 'application/json'},
            )

    def parse(self, response, subreddit):
        data = json.loads(response.text)
        posts = data['data']['children']
        word_counts = Counter()

        for post in posts:
            post_data = post['data']
            item = RedditscraperItem()
            item['title'] = post_data['title']
            item['link'] = post_data['url']
            item['posting_time'] = post_data['created_utc']
            item['score'] = post_data['score']
            item['num_comments'] = post_data['num_comments']
            item['subreddit'] = post_data['subreddit']
            yield item

            for word in post_data['title'].lower().split():
                word = word.strip('.,!?;:\'"()[]{}').strip()
                if len(word) > 3:
                    word_counts[word] += 1

        self._plot_word_frequency(word_counts, subreddit)

    def _plot_word_frequency(self, word_counts, subreddit):
        top = dict(word_counts.most_common(30))
        Path('output').mkdir(exist_ok=True)
        fig, ax = plt.subplots(figsize=(18, 8))
        ax.bar(range(len(top)), list(top.values()), color='#FF4500')
        ax.set_xticks(range(len(top)))
        ax.set_xticklabels(list(top.keys()), rotation=90)
        ax.set_title(f'Top Word Frequencies: r/{subreddit}')
        ax.set_ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'output/word_freq_{subreddit}.png', dpi=150)
        plt.close()
