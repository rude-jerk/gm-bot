from functools import wraps

from disnake import Embed, ApplicationCommandInteraction as Inter


def logged(command):
    @wraps(command)
    async def _impl(self, inter: Inter, *args, **kwargs):
        await command(self, inter, *args, **kwargs)
        if self.bot.log_channel:
            embed = Embed(title=f"Bot command from {inter.author}",
                          description=inter.data.name + ' ' + str(inter.filled_options))
            await self.bot.log_channel.send(embed=embed)

    return _impl
