### Summary

#PLEASE RUN THIS PROGRAM AND CHECK FOR ERRORS

# This is where you will set up configurations for your server
# This step is crucial for the program to work
# Please watch my tutorial at 

# -------------------------------------------------

#IGNORE THIS
#tesseractexe_location error: pytesseract.pytesseract.tesseract_cmd = r"C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe"


chrome_driver_path = "./chromedriver.exe"
# To get this key go to https://discord.com/developers/applications/
# Click on bot
# Copy token
discord_bot_token = "NzU0MTc4NzcyOTIzNTgwNDI3.X1w9tw.OgQNOZR539utGCY6Zk_CyxowILc"
discord_channel = "https://discord.com/channels/754154424863031327/754211093538144326"
discord_owner_id = 282205924804788224

screen_resolution = "2560x1080"

adjust_x = 0 # Adjust height of first grab (This grabs keywords for 'defeat', 'victory', 'imposter', 'crewmate')
adjust_y = -10

adjust_x_2 = 0 #Adjust height of cropped image (This is for keywords such as 'voting soon', 'whos the imposter?')
adjust_y_2 = 0

x_extend_crop = 150#pixels
y_extend_crop = 50#pixels

monitor_number = 1 

delay_start = 0  # adjust time delay from when you get imposter/crewmate till round start. 1 = one second more delay, -0.5 = 0.5 seconds less time
delay_voting = 0  # adjust time delay for when voting is ended to when the round starts

# time_delay is added or taken away from the delay set between when the screen 
# shows imposter, crewmate, or vote ended to when the round starts

debug_mode = False #Shows parsed output coming from image to text algorithm
debug_screen = 1 # 1 = shows what your program is seeing for screen grab of the keywords for 'defeat', 'victory', 'imposter', 'crewmate'
                 # 2 = shows what your program is seeing for screen that grabs keywords of 'voting soon', 'whos the imposter?'

# -------------------------------------------------

if __name__ == "__main__":
    try:
        import pytesseract # pip3 install pytesseract
        import threading 
        import selenium #pip3 install selenium
        import numpy
        import time
        import PIL # python3 -m pip install Pillow
        import mss # python3 -m pip install -U --user mss
        import cv2 # pip install opencv-python
        import os

        print("[*] No errors, your good to go!")
    except Exception as e: 
        print(f"{e}\n\n[*] Looks like your missing dependancies\n[*] Watch: ")
        exit()
