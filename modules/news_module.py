import praw
import discord
import asyncio
from datetime import datetime, timedelta
from . import Module

class NewsModule(Module):
    def __init__(self, client, reddit_client_id, reddit_client_secret, reddit_user_agent):
        super().__init__(client)
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent
        )
        self.last_rising_posts = []

    async def on_ready(self):
        await self.check_rising_news()

        # Schedule the routine to run every 10 minutes
        while True:
            await asyncio.sleep(600)  # Sleep for 10 minutes
            await self.check_rising_news()

    async def check_rising_news(self):
        subreddit_name = "technews"
        subreddit = self.reddit.subreddit(subreddit_name)
        rising_posts = subreddit.rising(limit=5)

        new_post = next(rising_posts, None)
        if new_post:
            if not self.is_duplicate(new_post):
                await self.post_news(new_post)

    def is_duplicate(self, new_post):
        top_post = self.last_rising_posts[0] if self.last_rising_posts else None
        return top_post and new_post.title == top_post.title

    async def post_news(self, new_post):
        channel_name = "news"  # Update with the name of your channel
        guild = discord.utils.get(self.client.guilds, name="Tinker.ai")  # Update with your guild name
        channel = discord.utils.get(guild.channels, name=channel_name)
        if channel:
            await channel.send(f"New rising news article: {new_post.title}\n{new_post.url}")

        self.last_rising_posts.insert(0, new_post)
        self.last_rising_posts = self.last_rising_posts[:5]  # Keep track of only the last 5 rising posts

    async def on_message(self, message):
        if message.content.startswith('!news'):
            await self.post_last_rising_posts(message)

    async def post_last_rising_posts(self, message):
        response = "\n".join(f"- {post.title}\n{post.url}" for post in self.last_rising_posts)
        await message.channel.send(response)
