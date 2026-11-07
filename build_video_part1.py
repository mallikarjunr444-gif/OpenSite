"""
OpenSite Demo Video Generator
Renders 1080p slide cards for Scenes 1 to 7, synthesizes audio, and encodes OpenSite_Demo_Video.mp4.
"""
import os
import sys
import math
import struct
import wave
import subprocess
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = "/Users/malikarjunr/hack"
ASSETS_DIR = os.path.join(BASE_DIR, "video_assets")
FRAMES_DIR = os.path.join(ASSETS_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)
FINAL_VIDEO = os.path.join(BASE_DIR, "OpenSite_Demo_Video.mp4")

BG = (9, 10, 8)
PANEL = (18, 19, 15)
PANEL_HI = (23, 24, 18)
LINE = (40, 41, 35)
LIME = (213, 255, 130)
WHITE = (244, 244, 241)
MUTED = (133, 134, 127)
CARD = (21, 22, 16)
HOVER = (67, 70, 58)
TEXT_MUT = (180, 181, 173)
CYAN = (130, 230, 255)

def get_font(path, sz):
    try: return ImageFont.truetype(path, sz)
    except: return ImageFont.load_default()

F_TITLE = get_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 44)
F_HERO = get_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
F_SUB = get_font("/System/Library/Fonts/HelveticaNeue.ttc", 24)
F_BODY = get_font("/System/Library/Fonts/HelveticaNeue.ttc", 19)
F_BOLD = get_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 19)
F_METRIC = get_font("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
F_TAG = get_font("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
F_NARR = get_font("/System/Library/Fonts/HelveticaNeue.ttc", 19)
F_CODE = get_font("/System/Library/Fonts/Supplemental/Arial.ttf", 16)

def header(d, sc_num, sc_title, time_code):
    d.rectangle([(0, 0), (1920, 80)], fill=PANEL)
    d.line([(0, 80), (1920, 80)], fill=LINE, width=2)
    d.text((50, 22), "OpenSite", fill=WHITE, font=F_TITLE)
    d.ellipse([(270, 36), (280, 46)], fill=LIME)
    d.text((295, 30), "SEO & CONVERSION INTELLIGENCE AGENT", fill=MUTED, font=F_TAG)
    badge = f"SCENE {sc_num:02d} · {time_code} · {sc_title.upper()}"
    d.rounded_rectangle([(1410, 20), (1870, 60)], radius=6, fill=PANEL_HI, outline=LINE)
    d.text((1430, 29), badge, fill=LIME, font=F_TAG)

def teleprompter(d, text, spk="Mallikarjun · OpenSite Creator"):
    d.rectangle([(0, 930), (1920, 1080)], fill=PANEL)
    d.line([(0, 930), (1920, 930)], fill=LINE, width=2)
    d.rounded_rectangle([(50, 945), (320, 975)], radius=6, fill=(24, 32, 15), outline=(72, 93, 46))
    d.text((65, 952), f"🎙 {spk}", fill=LIME, font=F_TAG)
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        if len(cur + " " + w) < 135: cur += (" " if cur else "") + w
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    y = 985
    for l in lines[:3]:
        d.text((65, y), l, fill=WHITE, font=F_NARR)
        y += 26

def card(d, x, y, w, h, t=None, sub=None, border=LINE, fill=CARD):
    d.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=fill, outline=border, width=1)
    if t: d.text((x + 24, y + 20), t, fill=WHITE, font=F_BOLD)
    if sub:
        d.text((x + 24, y + 46), sub, fill=MUTED, font=F_TAG)
        d.line([(x + 24, y + 70), (x + w - 24, y + 70)], fill=LINE, width=1)
