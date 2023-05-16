from BotHelpCommand import BotHelpCommand
from discord.ext import commands
import discord
from typing import List
from discord.utils import get
import asyncio


class BotClient(commands.Bot):
    def __init__(self, owner_id):
        commands.Bot.__init__(self, owner_id=owner_id, command_prefix=".", case_insensitive=True,
                              help_command=BotHelpCommand())
        self.ghostmode = False
        self.dead_members: List[discord.Member] = []
        self.in_channel: List[discord.Member] = []  # whoever is in the channel
        self.channel_connected = None
        self.connected = False

    async def on_ready(self):
        activity = discord.Game(name=".help", type=3)
        await self.change_presence(status=discord.Status.idle,
                                   activity=activity)
        print("Bot ready!")

    async def mute(self):
        """
            Called in the Tasks State, unmutes everyone but dead members

            :return:
        """
        async def mute_member(bot: BotClient, member: discord.Member):
            if member.voice is None:
                return
            elif member not in bot.in_channel:
                return
            elif member in bot.dead_members and bot.ghostmode:
                await member.edit(mute=False, deafen=False)
                # await member.edit(deafen=False)
                return
            else:
                print(f"[*] Muting: {member}")
                data = {"mute": True}
                if bot.ghostmode:
                    data['deafen'] = True
                await member.edit(**data)
                # if bot.ghostmode:
                #    await member.edit(deafen=True)
        await asyncio.gather(*[mute_member(self, member) for member in self.get_all_members()])

        """try:
            for member in list(self.get_all_members()):
                if member.voice is None:
                    continue
                elif member not in self.in_channel:
                    continue
                elif member in self.in_channel and member in self.dead_members and self.ghostmode:
                    await member.edit(mute=False)
                    await member.edit(deafen=False)
                    continue
                else:
                    print(f"[*] Muting: {member}")
                    await member.edit(mute=True)
                    if self.ghostmode:
                        await member.edit(deafen=True)

        except Exception as e:
            print(e)"""

    async def unmute(self):
        """
        Called in the Discussion State, unmutes everyone but dead members
        
        :return:
        """
        async def unmute_member(bot: BotClient, member: discord.Member):
            if member.voice is None:
                return
            if member not in bot.in_channel:
                return
            if member in bot.dead_members and bot.ghostmode:
                await member.edit(mute=True, deafen=False)
                return
            elif member in bot.dead_members:
                await member.edit(mute=True)
                return
            elif member in bot.in_channel:
                print(f"[*] Unmuting: {member}")
                data = {'mute': False}
                if bot.ghostmode:
                    data['deafen'] = False
                await member.edit(**data)
                # if bot.ghostmode:
                #     await member.edit(deafen=False)

        await asyncio.gather(*[unmute_member(self, member) for member in self.get_all_members()])
        """for member in list(self.get_all_members()):
            if member in self.in_channel and member in self.dead_members and self.ghostmode:
                await member.edit(mute=True)
                continue
            if member.voice is None:
                continue
            elif member in self.dead_members:
                continue
            elif member in self.in_channel:
                print(f"[*] Unmuting: {member}")
                await member.edit(mute=False, deafen=False)
                # if self.ghostmode:
                #    await member.edit(deafen=False)
            else:
                pass"""

    async def unmute_and_clear(self):
        self.dead_members.clear()
        await self.unmute()
        """for member in list(self.get_all_members()):
            if member.voice is None:
                continue
            elif member not in self.in_channel:
                continue
            else:
                print(f"[*] Unmuting: {member}")
                await member.edit(mute=False)"""

    def kill(self, player_name: str):
        for member in list(self.get_all_members()):
            if player_name == member.display_name:
                self.dead_members.append(member)

    async def set_colors(self, players_data):
        if len(self.in_channel) == 0:
            return
        author = self.in_channel[0]
        colors_dict = {
            "white": get(author.guild.roles, name='Branco'),
            "red": get(author.guild.roles, name='Vermelho'),
            "orange": get(author.guild.roles, name='Laranja'),
            "green": get(author.guild.roles, name='Verde Claro'),
            "lime": get(author.guild.roles, name='Verde Escuro'),
            "cyan": get(author.guild.roles, name='Azul Claro'),
            "azul": get(author.guild.roles, name='Azul Escuro'),
            "pink": get(author.guild.roles, name='Rosa'),
            "black": get(author.guild.roles, name='Preto'),
            "yellow": get(author.guild.roles, name='Amarelo'),
            "brown": get(author.guild.roles, name='Marrom'),
            "purple": get(author.guild.roles, name='Roxo'),
        }

        async def set_member_color(set_member: discord.Member, color: str):
            print(f"Setting color '{color}' for {set_member.display_name}...")
            color = " ".join(color).strip().lower().replace(" ", "")
            print(colors_dict)
            if color not in colors_dict:
                print("This color does not exist")
                return
            if colors_dict[color] in set_member.roles:
                print("Member colors was already right")
                return

            color_role = colors_dict[color]

            print(f"Found color '{color_role.name}' with '{color}'")

            async def remove_role(removed_role):
                if removed_role in set_member.roles:
                    await set_member.remove_roles(removed_role)
                print(f"Color {removed_role.name} removed")

            await asyncio.gather(*[remove_role(role) for role in colors_dict.values()])
            await set_member.add_roles(color_role)

        members_colors = dict()
        for member in self.in_channel:
            for member_data in players_data['players']:
                if member_data['name'] == member.display_name:
                    members_colors[member] = member_data['color']

        await asyncio.gather(*[set_member_color(member, color) for member, color in members_colors.items()])