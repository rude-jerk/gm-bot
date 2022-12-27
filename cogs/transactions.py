from disnake import ApplicationCommandInteraction as Inter
from disnake.ext import commands

import settings
from db_util import closing
from log_util import logged
from queries import dbox_hist

lb = "\n"


def build_hist_msg(recs):
    return_list = []
    for i in recs:
        return_list.append(f"{i.sender_name}->{i.receiver_name} "
                           f"[{i.name}]{f' x{i.quantity}' if i.quantity > 1 else ''}")

    return return_list


class Transactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='dbox_history',
                            description='Retrieves the most recent outgoing and incoming delivery box transactions',
                            dm_permission=False)
    @commands.has_role(int(settings.PERM_ROLE))
    @logged
    async def dbox_history(self, inter: Inter,
                           character: str = commands.Param(max_length=20),
                           size: int = commands.Param(default=10, max_value=20),
                           private: bool = commands.Param(default=True)):
        await inter.response.defer(with_message=True, ephemeral=private)

        with closing(self.bot.db_pool.get_connection()) as cnx:
            with closing(cnx.cursor(named_tuple=True)) as cursor:
                cursor.execute(dbox_hist.format(limit=size, where='WHERE sender_name = %s'), (character,))
                outgoing_rows = build_hist_msg([row for row in cursor])
                cursor.execute(dbox_hist.format(limit=size, where='WHERE receiver_name = %s'), (character,))
                incoming_rows = build_hist_msg([row for row in cursor])

        out_msg = f"Outgoing:\n```{lb.join(outgoing_rows)}```" if outgoing_rows else ''
        out_msg += f"\nIncoming:\n```{lb.join(incoming_rows)}```" if incoming_rows else ''
        await inter.followup.send(out_msg if out_msg != '' else 'No delivery box transactions.')


def setup(bot):
    bot.add_cog(Transactions(bot))
