#!/usr/bin/env python3
"""
\033[96m📸 PixelPlanet Timelapser\033[0m

\033[93mUsage:\033[0m
    \033[92mtimelapser.py startX_startY endX_endY canvasID website [no_compare] [timestamp]\033[0m
        (\033[95mUse the R key on PixelPlanet to copy coordinates\033[0m)

    \033[92mtimelapser.py canvases "website"\033[0m
        -> \033[95mFetches and lists canvases from a specific pixelplanet clone.\033[0m

    \033[92mtimelapser.py -h | --help\033[0m
        -> \033[95mShow this help message.\033[0m

Add "no_compare" as an argument to always save frames.
Add "timestamp" as an argument to add timestamp to each frame.
"""

import sys
import os
import io
import time
import json
import asyncio
import aiohttp
import PIL.Image
import logging
from PIL import ImageDraw, ImageFont
from datetime import datetime

RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
RESET   = "\033[0m"

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if not os.path.isdir("frame"):
    os.makedirs("frame")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)

# ===================== Classes =====================

class Color:
    def __init__(self, index: int, name: str, rgb: tuple):
        self.index = index
        self.name = name
        self.rgb = rgb

class GlobalColors:
    colors = []

    @staticmethod
    def index(i: int) -> Color:
        if 0 <= i < len(GlobalColors.colors):
            return GlobalColors.colors[i]
        return GlobalColors.colors[0]

class Matrix:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.width = None
        self.height = None
        self.matrix = {}
        self.use_timestamp = False

    def add_coords(self, x: int, y: int, w: int, h: int):
        if self.start_x is None or x < self.start_x:
            self.start_x = x
        if self.start_y is None or y < self.start_y:
            self.start_y = y
        end_x = x + w
        end_y = y + h

        if self.width is None or self.height is None:
            self.width = w
            self.height = h
        else:
            current_end_x = self.start_x + self.width
            current_end_y = self.start_y + self.height
            self.width = max(current_end_x, end_x) - self.start_x
            self.height = max(current_end_y, end_y) - self.start_y

    def set_pixel(self, x: int, y: int, color: Color):
        if (self.start_x is None or self.start_y is None or
            x < self.start_x or x >= self.start_x + self.width or
            y < self.start_y or y >= self.start_y + self.height):
            return

        if x not in self.matrix:
            self.matrix[x] = {}
        self.matrix[x][y] = color

    def create_image(self, filename: str = None):
        """
        Create an image from the pixel matrix.
        If filename is 'b', returns a BytesIO buffer.
        """
        img = PIL.Image.new('RGBA', (self.width, self.height), (255, 0, 0, 0))
        pxls = img.load()
        for x in range(self.width):
            for y in range(self.height):
                actual_x = x + self.start_x
                actual_y = y + self.start_y
                try:
                    pixel_color = self.matrix[actual_x][actual_y].rgb
                    pxls[x, y] = pixel_color
                except (KeyError, AttributeError):
                    continue
        
        # Add timestamp overlay if enabled
        if self.use_timestamp:
            try:
                draw = ImageDraw.Draw(img)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                font_size = 32 
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    try:
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                    except IOError:
                        try:
                            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                        except IOError:
                            font = ImageFont.load_default()
                
                text_width, text_height = draw.textbbox((0, 0), current_time, font=font)[2:4]
                padding = 10
                
                draw.rectangle(
                    (
                        padding, 
                        padding, 
                        padding + text_width + padding, 
                        padding + text_height + padding
                    ), 
                    fill=(80, 80, 80, 255),
                    outline=(220, 220, 220, 200)
                )
                
                shadow_offset = 1
                draw.text((padding + shadow_offset + 2, padding + shadow_offset + 2), 
                        current_time, fill=(30, 30, 30, 200), font=font)  # Shadow
                draw.text((padding + 2, padding + 2), 
                        current_time, fill=(240, 240, 240, 255), font=font)  # Main text
            except Exception as e:
                logging.warning(f"{YELLOW}⚠️ Could not add timestamp: {e}{RESET}")

        if filename:
            if filename == 'b':
                b = io.BytesIO()
                img.save(b, "PNG")
                b.seek(0)
                img.close()
                return b
            else:
                img.save(filename)
                logging.info(f"{GREEN}💾 Image saved as {filename}{RESET}")
        else:
            img.show()
        img.close()

dim = {
    0: [256],
    1: [64],
    3: [16],
    5: [128],
    6: [128],
    7: [256]
}

# ===================== Canvas Functions =====================

async def fetch_canvas_colors(canvas_id: int, website: str) -> list:
    url = f"https://{website}/api/me"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            j = json.loads(data)
    canvases = j.get("canvases", {})
    canvas = canvases.get(str(canvas_id))
    if canvas is None:
        raise Exception(f"{RED}❌ Canvas {canvas_id} not found in API response{RESET}")

    colors = []
    for i, col in enumerate(canvas.get("colors", [])):
        r, g, b = col
        colors.append(Color(i, f"color{i}", (r, g, b, 255)))
    logging.info(f"{GREEN}🌈 Fetched canvas colors successfully!{RESET}")
    return colors

async def list_canvases(website: str):
    url = f"https://{website}/api/me"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()
            j = json.loads(data)
    canvases = j.get("canvases", {})
    if not canvases:
        print(f"{RED}No canvases found.{RESET}")
        return
    print(f"{GREEN}Canvases:{RESET}")
    for cid, info in canvases.items():
        title = info.get("title", "N/A")
        if title == "3D Canvas":
            continue
        print(f"  {YELLOW}ID: {cid}{RESET}  {BLUE}Title: {title}{RESET}")

# ===================== Tiles Functions =====================

async def fetch(session: aiohttp.ClientSession, ix: int, iy: int,
                target_matrix: Matrix, canvas_id: int, website: str):
    tile_size = 256
    url = f"https://{website}/chunks/{canvas_id}/{ix}/{iy}.bmp"
    attempts = 0

    while True:
        try:
            async with session.get(url) as resp:
                data = await resp.read()
            offset = int(-dim[canvas_id][0] ** 2 / 2)
            off_x = ix * tile_size + offset
            off_y = iy * tile_size + offset

            if len(data) == 0:
                clr = GlobalColors.index(0)
                for i in range(tile_size * tile_size):
                    tx = off_x + (i % tile_size)
                    ty = off_y + (i // tile_size)
                    target_matrix.set_pixel(tx, ty, clr)
            else:
                for i, b in enumerate(data):
                    tx = off_x + (i % tile_size)
                    ty = off_y + (i // tile_size)
                    if b > 127:
                        c = b - 128
                        pixel = GlobalColors.index(c).rgb
                        avg = int((pixel[0] + pixel[1] + pixel[2]) / 3)
                        target_matrix.set_pixel(tx, ty, Color(0, 'gray', (avg, avg, avg, 225)))
                    else:
                        target_matrix.set_pixel(tx, ty, GlobalColors.index(b))
            logging.info(f"{GREEN}✅ Loaded {url} with {len(data)} bytes{RESET}")
            break

        except Exception as e:
            attempts += 1
            if attempts > 3:
                logging.error(f"{RED}❌ Error loading {url}: {e}{RESET}")
                raise
            logging.info(f"{YELLOW}🔄 Retrying {url} (attempt {attempts}){RESET}")
            await asyncio.sleep(1)

async def get_area(session: aiohttp.ClientSession, x: int, y: int, w: int, h: int, canvas_id: int, website: str) -> Matrix:
    target_matrix = Matrix()
    target_matrix.add_coords(x, y, w, h)
    tile_size = 256
    offset = int(-dim[canvas_id][0] ** 2 / 2)

    xc = (x - offset) // tile_size
    yc = (y - offset) // tile_size
    wc = (x + w - offset) // tile_size
    hc = (y + h - offset) // tile_size

    logging.info(f"{CYAN}🧩 Loading tiles from ({xc}, {yc}) to ({wc}, {hc}) for canvas {canvas_id}{RESET}")

    tasks = []
    for iy in range(yc, hc + 1):
        for ix in range(xc, wc + 1):
            tasks.append(fetch(session, ix, iy, target_matrix, canvas_id, website))
    await asyncio.gather(*tasks)
    return target_matrix

# ===================== Main Functions =====================

async def timelapsing():
    if len(sys.argv) < 5:
        print(f"{CYAN}{__doc__}{RESET}")
        sys.exit(1)

    start = sys.argv[1].split('_')
    end = sys.argv[2].split('_')
    base_filename = "t"
    canvas_id = int(sys.argv[3])
    website = sys.argv[4]

    no_compare = False
    use_timestamp = False
    
    # Process optional arguments
    for arg in sys.argv[5:]:
        if arg.lower() == "no_compare":
            no_compare = True
        elif arg.lower() == "timestamp":
            use_timestamp = True

    x = int(start[0])
    y = int(start[1])
    w = int(end[0]) - x
    h = int(end[1]) - y

    GlobalColors.colors = await fetch_canvas_colors(canvas_id, website)

    prev_pixels = None
    iteration = 1

    connector = aiohttp.TCPConnector(limit=20)
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            matrix = await get_area(session, x, y, w, h, canvas_id, website)
            
            # Set timestamp flag in the matrix object
            matrix.use_timestamp = use_timestamp
            
            image_buffer = matrix.create_image('b')
            image_buffer.seek(0)
            new_img = PIL.Image.open(image_buffer)
            curr_pixels = list(new_img.getdata())

            filename = f"frame/{base_filename}{iteration}.png"
            if not no_compare:
                if prev_pixels is not None and curr_pixels == prev_pixels:
                    logging.info(f"{YELLOW}🤷‍♂️ No pixel changes detected. Skipping frame {filename}{RESET}")
                else:
                    with open(filename, 'wb') as f:
                        f.write(image_buffer.getvalue())
                    logging.info(f"{BLUE}🖼️  Frame {iteration} saved as {filename}{RESET}")
                    prev_pixels = curr_pixels
                    iteration += 1
            else:
                with open(filename, 'wb') as f:
                    f.write(image_buffer.getvalue())
                logging.info(f"{BLUE}🖼️  Frame {iteration} saved as {filename} (no_compare enabled){RESET}")
                prev_pixels = curr_pixels
                iteration += 1
            await asyncio.sleep(0.05)

async def main():

    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(f"{CYAN}{__doc__}{RESET}")
        sys.exit(0)

    if len(sys.argv) >= 2 and sys.argv[1] == "canvases":
        website = sys.argv[2] if len(sys.argv) > 2 else "pixelplanet.fun"
        await list_canvases(website)
        sys.exit(0)

    await timelapsing()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(f"{MAGENTA}👋 Terminated by user.{RESET}")
