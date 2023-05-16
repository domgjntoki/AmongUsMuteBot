### Summary

# This module takes an input as an image, converts the image to a string and determines 
# the game state and if the channel should be muted or unmuted and passes this to the 
# send command module

# -------------------------------------------------

from modules.config import *
import pytesseract  # pip3 install pytesseract
import time

# If you are getting pytesseract error, change r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# to r"C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe" and  change USER to you computer name
pytesseract.pytesseract.tesseract_cmd = r"F:\Light Development\Tesseract-OCR\tesseract.exe"

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Process:
    def __init__(self, bot):
        self.bot = bot

    async def process_discussion(self, image: complex):
        found = False
        delay = 6

        delay_voting = 7  # Delay between voting ends and round starting
        discussion = {"?","impestoe","who",'whos',"wino","innoosttor?","imsoster?","inostor?","imposter?","inyoostor?","iniposior?","inijposior?","impostor?","inoster?","tnrpester?","tnsester?","inraostor?","inaoster?","tnsoster?","tnpester?",'hnnsester?'}
        voting = {"voting", "results","result","vetting","vartine","votingiresults","vetting)"}

        raw_output = pytesseract.image_to_string(image)

        if debug_mode:
            print(raw_output.strip().lower())

        out = set(raw_output.strip().lower().split(" "))

        if len(out.intersection(discussion)) != 0: #if one of the keywords for discussion time is present
            found = True
            print("DISCUSSION [UNMUTED]")
            await self.bot.unmute()

            return found

        elif len(out.intersection(voting)) != 0: #if one of the keywords for ended voting is present
            found = True
            print("VOTING ENDED [MUTING SOON]")

            time.sleep(delay + delay_voting)
            await self.bot.mute() #mute

            return found
        else:
            return found

    async def process_ending(self, image: complex):
        delay = 3.5 #Delay between getting role and game starting

        defeat = {"defeat","deteat"}
        victory = {"victory","vicory","viton"}
        imposter = {"imposter","impostor","tmonetor"}
        crewmate = {"crewmate"}

        raw_output = pytesseract.image_to_string(image)

        if debug_mode:
            print(raw_output.strip().lower())

        out = set(raw_output.strip().lower().split(" "))

        if len(out.intersection(defeat)) != 0:  # if one of the keywords for defeat is present
            print("DEFEAT [UNMUTED]")
            await self.bot.unmute_and_clear()  # unmute everyone including the dead

        elif len(out.intersection(victory)) != 0:  # if one of the keywords for victory is present
            print("VICTORY [UNMUTED]")
            await self.bot.unmute_and_clear()  # unmute everyone including the dead

        elif len(out.intersection(crewmate)) != 0:  # if one of the keywords for crewmate is present
            print("YOU GOT CREWMATE [MUTING SOON]")

            time.sleep(delay + delay_start)
            await self.bot.mute()  # mute

        elif len(out.intersection(imposter)) != 0:  # if one of the keywords for imposter is present
            print("YOU GOT IMPOSTER [MUTING SOON]")

            time.sleep(delay + delay_start)
            await self.bot.mute()  # mute
        else:
            pass
