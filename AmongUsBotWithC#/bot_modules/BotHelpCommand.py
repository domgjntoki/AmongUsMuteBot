from discord import Embed
from discord.ext import commands
from typing import Dict, List


class BotHelpCommand(commands.HelpCommand):
    def __init__(self):
        commands.HelpCommand.__init__(self)

    async def send_bot_help(self, mapping: Dict[commands.Cog, List[commands.core.Command]]):
        embed = Embed(title="Lista de Comandos")
        n = 0
        commands_per_row = 1
        for cog, coms in mapping.items():
            if cog is not None:
                for command in coms:
                    if command.hidden:
                        continue
                    if n % commands_per_row == 0:
                        embed.add_field(name=command.qualified_name,
                                        value=f"{command.brief}",
                                        inline=False)
                    else:
                        embed.add_field(name=command.qualified_name,
                                        value=f"{command.brief}")
                    n += 1
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog: commands.Cog):
        print(cog)
