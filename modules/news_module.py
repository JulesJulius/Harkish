import praw
import discord
import asyncio
import pickle
from datetime import datetime, timedelta
from . import Module

class NewsModule(Module):
    def __init__(self, client, reddit_client_id, reddit_client_secret, reddit_user_agent):
        super().__init__(client)
        
        self.news_channel = 'news'

        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent
        )
        self.posted_news_file = "posted_news.pkl"
        try:
            with open(self.posted_news_file, "rb") as file:
                self.posted_news = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.posted_news = set()

    async def on_ready(self):
        await self.check_rising_news()

        # Schedule the routine to run every 10 minutes
        while True:
            await asyncio.sleep(600)  # Sleep for 10 minutes
            await self.check_rising_news()

    async def check_rising_news(self):
        subreddit_name = "technews"
        subreddit = self.reddit.subreddit(subreddit_name)
        rising_posts = subreddit.rising(limit=1)

        for new_post in rising_posts:
            if new_post.id not in self.posted_news:
                await self.post_news(new_post)

    async def post_news(self, new_post):
        channel_name = self.news_channel  # Update with the name of your channel
        guild = discord.utils.get(self.client.guilds, name="Tinker.ai")  # Update with your guild name
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel:
            await channel.send(f"New rising news article: {new_post.title}\n{new_post.url}")

        self.posted_news.add(new_post.id)
        with open(self.posted_news_file, "wb") as file:
            pickle.dump(self.posted_news, file)

    async def on_message(self, message):
        if message.content.startswith('!news'):
            await self.post_last_rising_posts(message)

    async def post_last_rising_posts(self, message):
        response = "\n".join(f"- {post.title}\n{post.url}" for post in self.last_rising_posts)
        await message.channel.send(response)
