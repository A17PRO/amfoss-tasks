import os
import subprocess
import textwrap
import time
import glob

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter
from google import genai
from dotenv import load_dotenv
from datetime import datetime

#FUNCTIONS
def draw_time(draw, time_str, font, color):
    draw.text((1600, 100), time_str, font=font, fill=color)


def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return "File not found"

def draw_notes(draw, text, font, color):
    lines = text.split('\n')

    wrapped_lines = []
    for line in lines:
        wrapped_chunks = textwrap.wrap(line, width = 45)
        wrapped_lines.extend(wrapped_chunks)

    formatted_text = "\n".join(wrapped_lines)
    draw.multiline_text((100, 100), formatted_text, font=font, fill=color, spacing = 15)



#EXECUTION - MAIN CODE
def main():
    try:
        while True:
            try:
                #init
                canvas = Image.new("RGB", (1920, 1080), ImageColor.getrgb("#000000"))
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
                time_str = datetime.now().strftime("%H:%M:%S")

                #draw time
                draw = ImageDraw.Draw(canvas)
                draw_time(draw, time_str, font, (255,255,255))

                #draw notes
                notes = read_file("to-do-list.txt")
                draw_notes(draw, notes, font, (255, 255, 255))

                #save wallpaper
                unique_id = time_str
                wallpaper_path = f"wallpaper_{unique_id}.jpg"
                canvas.save(wallpaper_path)
                print(f"Saved successfully to {wallpaper_path}")

                #apply wallpaper
                abs_path = os.path.abspath(wallpaper_path)
                subprocess.run(["plasma-apply-wallpaperimage", abs_path], check=True)
                print("Wallpaper Applied")

                #delete images
                for old_file in glob.glob("wallpaper_*.jpg"):
                    if old_file != wallpaper_path:
                        os.remove(old_file)
                        print("Cleaned up files")
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEngine stopped")


if __name__ == "__main__":
    main()
