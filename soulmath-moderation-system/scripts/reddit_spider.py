import scrapy
import json

class RedditSpider(scrapy.Spider):
    name = "reddit"

    def __init__(self, subreddit="technology", limit=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"]

    def parse(self, response):
        data = json.loads(response.text)
        for child in data.get("data", {}).get("children", []):
            post = child["data"]
            yield {
                "id": post.get("id"),
                "title": post.get("title"),
                "selftext": post.get("selftext"),
                "author": post.get("author"),
                "created": post.get("created_utc"),
                "subreddit": post.get("subreddit"),
            }

