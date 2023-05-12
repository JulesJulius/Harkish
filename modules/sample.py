from . import Module

class SampleModule(Module):
    async def on_message(self, message):
        if message.content.startswith('!hello'):
            await message.channel.send('Hello!')
