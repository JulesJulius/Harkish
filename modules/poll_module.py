from .import Module
import discord
from discord.ext import commands
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

class PollModule(Module):

    async def on_message(self, msg):
        if msg.content.startswith('!poll'):
            prompt = "On the topic of AI and technology, a divisive agree or disagree question one could ask a group of technologists would be worded something like:"
            completion = self.generate_completion(prompt)
            poll_question = self.extract_poll_question(completion)
            await self.send_poll(msg.channel, poll_question)

    def generate_completion(self, prompt):
        response = openai.Completion.create(
            engine='davinci',
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()

    def extract_poll_question(self, completion):
        question = completion.split("\n\n")[0]
        return question

    async def send_poll(self, channel, question):
        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        poll_message = await channel.send(embed=embed)
        await poll_message.add_reaction('👍')
        await poll_message.add_reaction('👎')
