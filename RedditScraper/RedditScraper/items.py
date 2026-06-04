import scrapy


class RedditscraperItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    posting_time = scrapy.Field()
    score = scrapy.Field()
    num_comments = scrapy.Field()
    subreddit = scrapy.Field()
