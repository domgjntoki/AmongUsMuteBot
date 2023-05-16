from discord.ext import commands
import discord
import BotClient
import json
from typing import Optional


class BotCommands(commands.Cog, name="Comandos"):
    def __init__(self, bot: BotClient):
        self.bot = bot

    @commands.command(brief="Lista todos os membros no canal")
    async def members(self, ctx):
        if len(self.bot.in_channel) == 0:
            await ctx.send("[*] Não há membros conectados a esse canal")
            await ctx.send("[*] todo membro deve usar .join NOME_DO_CANAL")
        else:
            all_members = "[*] Lista das pessoas conectadas, se seu nome está faltando digite .join\n"
            for member in self.bot.in_channel:
                all_members = all_members + f" - {member.display_name}\n"

            await ctx.send(all_members)

    @commands.command(brief="Todo jogador deve se conectar ao canal usando esse comando")
    async def join(self, ctx, member: Optional[discord.Member] = None):
        if member is None:
            member = ctx.author

        try:
            if member in self.bot.in_channel:
                await ctx.send("[*] Você já está nesse canal")
            else:
                await ctx.send(f'[*] "{member.display_name}" foi adicionado a {self.bot.channel_connected}')
                self.bot.in_channel.append(member)

        except Exception as e:
            print(e)
            await ctx.send("[*] Você não está conectado a nenhum canal")

    @commands.command(brief="Para ver se o bot está online!")
    async def ping(self, ctx):
        await ctx.send("[*] Pong")

    @commands.command(brief="Desconecta do canal atual")
    async def disconnect(self, ctx):
        try:
            if ctx.author.name in self.bot.in_channel:
                print("[*] Você foi removido!")
                self.bot.in_channel.remove(ctx.author)

        except Exception as e:
            print(f"[*] ERROR: {e}")
            await ctx.send(f"[*] Algo deu errado, cheque os logs no cmd")

    @commands.command(brief="Use esse comando se morrer, então ficará mudo na discursões e falará com outros mortos "
                            "em jogo! (Não precisa mais)",
                      hidden=True)
    async def dead(self, ctx, member: discord.Member = None):
        if member is None:
            author = ctx.author
        else:
            author = member
        if author.name in self.bot.in_channel and author.name not in self.bot.dead_members:
            self.bot.dead_members.append(author)

    @commands.command(brief=".channel NOME_DO_CANAL -> Conecta o Bot à esse canal")
    async def channel(self, ctx, arg):
        connected = False
        for channel in self.bot.get_all_channels():
            if arg.lower() == str(channel).lower():
                await ctx.send(f"[*] Bot conectado com sucesso a {arg}")

                self.bot.channel_connected = channel
                connected = True
        if not connected:
            await ctx.send(f"[*] Canal não encontrado : {arg}")

    @commands.command(brief="Adiciona todos no canal de voz ao canal")
    async def setup(self, ctx):
        final_str = ""
        for member in self.bot.channel_connected.members:
            if member in self.bot.in_channel:
                final_str += f"- '{member.display_name}' já estava conectado à {self.bot.channel_connected.name}\n"
            else:
                final_str += f"- Conectando '{member.display_name}' à {self.bot.channel_connected.name}\n"
                self.bot.in_channel.append(member)
        await ctx.send(final_str)

    @commands.command(brief="Muta aúdio e voz de todos durante as rodadas, exceto os mortos (Para que eles possam "
                            "conversar entre si)")
    async def ghostmode(self, ctx):
        self.bot.ghostmode = not self.bot.ghostmode
        str_t = "ativado" if self.bot.ghostmode else "desativado"
        await ctx.send(f"[*] Ghostmode " + str_t)

    @commands.command(brief="Muta o audio de todos, exceto mortos no ghostmode ativado",
                      hidden=True)
    async def mute(self, ctx):
        await self.bot.mute()

    @commands.command(brief="Desmuta o áudio de todos, exceto de mortos",
                      hidden=True)
    async def unmute(self, ctx):
        await self.bot.unmute()

    @commands.command(brief="Seta a cor de todos os jogadores de acordo ao que está no Among Us",
                      hidden=True)
    async def set_colors(self, ctx):
        with open(r"F:\Desktop\Projetos\AmongUs\among.json") as data:
            js = json.load(data)
            await self.bot.set_colors(js)
