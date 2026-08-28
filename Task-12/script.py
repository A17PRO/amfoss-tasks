import os
import subprocess
import textwrap
import time
import glob
import threading

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter
from google import genai
from dotenv import load_dotenv
from datetime import datetime

#Functions
def draw_time(draw, time_str, font, color):
    draw.text((1600, 100), time_str, font=font, fill=color)

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    else:
        return "File not found"

def draw_notes(draw, text, font, color):
    draw.multiline_text((100, 100), text, font=font, fill=color, spacing=15)

def format(raw_text):
    """Runs in a background thread. Fetches AI formatting without stalling the clock."""
    global cached_ai_notes, is_ai_loading
    
    if not raw_text.strip():
        cached_ai_notes = "TASK                                      | IMPORTANCE\n1. Go play games.                         | HIGH"
        is_ai_loading = False
        return

    prompt = f"""
    You are a productivity assistant formatting a to-do list for a desktop wallpaper. 
    Format the raw notes into a crisp table using space padding to align the pipe '|' character.

    Format requirements:
    - Line 1 must be exact header: TASK                                      | IMPORTANCE
    - Keep task names short (truncate or summarize to under 35 characters).
    - Pad spaces so the '|' character aligns at EXACTLY column index 42 on every line.
    - Assign priority: HIGH, MED, or LOW.

    CRITICAL:
    - Do NOT use markdown code blocks (```).
    - Do NOT wrap lines or add extra line breaks inside a task item.
    - Output ONLY plain text.

    Raw notes:
    {raw_text}
    """
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        cached_ai_notes = response.text.strip()
    except Exception as e:
        print(f"AI Error (falling back to raw text): {e}")
        cached_ai_notes = raw_text
    finally:
        is_ai_loading = False
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        cached_ai_notes = response.text.strip()
    except Exception as e:
        print(f"AI Error (falling back to raw text): {e}")
        cached_ai_notes = raw_text
    finally:
        is_ai_loading = False

#Init AI
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
api_key = (
    os.getenv("GEMINI_API_KEY")
)
api_key = api_key.strip() if api_key else ""
if not api_key:
    raise RuntimeError(
        "No Gemini API key found. Add GEMINI_API_KEY to your .env file."
    )
ai_client = genai.Client(api_key=api_key)

#Cache
cached_ai_notes = "Loading tasks..."
is_ai_loading = False

#Main Code
def main():
    global cached_ai_notes, is_ai_loading
    file_path = "/home/aditya/amfoss-tasks/Task-12/to-do-list.txt"
    last_minute = ""
    last_mtime = 0
    last_rendered_notes = ""

    # Initial load of the file
    if os.path.exists(file_path):
        raw_notes = read_file(file_path)
        cached_ai_notes = raw_notes
        
    try:
        while True:
            try:
                current_minute = datetime.now().strftime("%H:%M")
                current_mtime = os.path.getmtime(file_path) if os.path.exists(file_path) else 0

                #AI Updating logic
                if current_mtime != last_mtime and not is_ai_loading:
                    print("File saved! Spawning AI thread...")
                    last_mtime = current_mtime
                    is_ai_loading = True
                    raw_notes = read_file(file_path)

                    threading.Thread(
                        target=format,
                        args=(raw_notes,), 
                        daemon=True
                    ).start()

                #init canvas
                canvas = Image.new("RGB", (1920, 1080), ImageColor.getrgb("#000000"))
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
                time_str = datetime.now().strftime("%H:%M:%S")

                #draw time
                draw = ImageDraw.Draw(canvas)
                draw_time(draw, time_str, font, (255,255,255))

                # Draw notes
                draw_notes(draw, cached_ai_notes, font, (255, 255, 255))

                #save wallpaper
                unique_id = datetime.now().strftime("%H:%M:%S")
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
        print("\nProgram stopped")

if __name__ == "__main__":
    main()
