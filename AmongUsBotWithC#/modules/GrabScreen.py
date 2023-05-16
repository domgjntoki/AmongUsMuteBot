### Summary

# This module grabs an image from the screen and funnels
# it to the processing module

# -------------------------------------------------

from mss import mss  # python3 -m pip install -U --user mss
import cv2  # pip install opencv-python
from PIL import Image  # python3 -m pip install Pillow
import numpy as np
from discord.ext import commands, tasks
from modules.module_process import Process
from modules.config import *


class GrabScreen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.x_resolution, self.y_resolution = int(screen_resolution.split("x")[0]), int(screen_resolution.split("x")[1])
        self.settings = {"top": int(0.08 * self.y_resolution) + adjust_y,
                         "left": int(self.x_resolution * 0.18) + adjust_x,
                         "width": int(self.x_resolution * 0.7), "height": int(0.25 * self.y_resolution),
                         "mon": monitor_number}
        self.process = Process(bot)

        self.x_crop = int(self.x_resolution * 0.18)
        self.y_crop = int(self.y_resolution * 0.08)
        self.first_time = True

    def return_frame(self, sct):
        # Take image of screen
        sct_img = sct.grab(self.settings)
        img = Image.frombytes('RGB', (sct_img.size.width, sct_img.size.height), sct_img.rgb)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        return frame

    @tasks.loop(seconds=1)
    async def grab_screen(self):
        with mss() as sct:
            frame = self.return_frame(sct)

            try:
                # Crop image to fit only "voting ended" and "whos the imposter?"
                cropped_frame = frame[10:(self.y_crop + y_extend_crop),
                                int(self.x_crop / 2 - x_extend_crop + 80):-int(self.x_crop / 2 + x_extend_crop)].copy()

                if debug_mode:
                    cv2.imshow('Test', np.array(frame))  # output screen, for testing only
                    cv2.imshow('Test Cropped', np.array(cropped_frame))  # output screen, for testing only

            except Exception as e:
                print(f"{e}\nLooks like your x_extend_crop or y_extend_crop values are way too high")
                exit()

            if self.first_time:
                print("Ready.\nYou can play now.\n")
                self.first_time = False

            # Process image
            found = await self.process.process_discussion(cropped_frame)

            if not found:  # If discussion or voting ends found, you dont need to process ending
                found = await self.process.process_ending(frame)

            if cv2.waitKey(25) & 0xFF == ord('q'):  # Press Q on debug windows to exit
                cv2.destroyAllWindows()
                return


if __name__ == "__main__":
    print("Please run start.py: ")
    exit()
