"""
OpenSite Demo Video Generator
Renders 1080p presentation frames and compiles the complete OpenSite product presentation video.
"""
import os
import math
import struct
import wave
import subprocess
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/malikarjunr/hack/video_production"
FRAMES_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

# Colors matching OpenSite design system
BG_COLOR = (9, 10, 8)          # #090a08
PANEL_COLOR = (18, 19, 15)      # #12130f
PANEL_HI = (23, 24, 18)         # #171812
LINE_COLOR = (40, 41, 35)       # #282923
LIME = (213, 255, 130)          # #d5ff82
WHITE = (244, 244, 241)         # #f4f4f1
MUTED = (133, 134, 127)         # #85867f
CARD_BG = (21, 22, 16)          # #151610
BORDER_HOVER = (67, 70, 58)     # #43463a
TEXT_MUTED = (180, 181, 173)    # #b4b5ad
CYAN_ACCENT = (130, 230, 255)
PURPLE_ACCENT = (200, 160, 255)

# Fonts
try:
    FONT_TITLE_BOLD = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    FONT_HERO = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 64)
    FONT_SUBTITLE = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 24)
    FONT_BODY = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    FONT_BODY_BOLD = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    FONT_METRIC = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 36)
    FONT_TAG = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    FONT_NARRATION = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    FONT_CODE = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
except Exception:
    FONT_TITLE_BOLD = ImageFont.load_default()
    FONT_HERO = ImageFont.load_default()
    FONT_SUBTITLE = ImageFont.load_default()
    FONT_BODY = ImageFont.load_default()
    FONT_BODY_BOLD = ImageFont.load_default()
    FONT_METRIC = ImageFont.load_default()
    FONT_TAG = ImageFont.load_default()
    FONT_NARRATION = ImageFont.load_default()
    FONT_CODE = ImageFont.load_default()

def draw_header(d, scene_num, scene_title, time_code):
    # Top bar
    d.rectangle([(0, 0), (1920, 80)], fill=PANEL_COLOR)
    d.line([(0, 80), (1920, 80)], fill=LINE_COLOR, width=2)
    
    # Logo
    d.text((50, 22), "OpenSite", fill=WHITE, font=FONT_TITLE_BOLD)
    d.ellipse([(280, 36), (290, 46)], fill=LIME)
    d.text((305, 30), "SEO & CONVERSION INTELLIGENCE AGENT", fill=MUTED, font=FONT_TAG)
    
    # Scene Indicator
    badge_text = f"SCENE {scene_num:02d} · {time_code} · {scene_title.upper()}"
    badge_w = 480
    d.rounded_rectangle([(1920 - badge_w - 50, 20), (1920 - 50, 60)], radius=6, fill=PANEL_HI, outline=LINE_COLOR)
    d.text((1920 - badge_w - 30, 29), badge_text, fill=LIME, font=FONT_TAG)

def draw_teleprompter(d, narration_text, speaker="Mallikarjun · OpenSite Creator"):
    # Bottom teleprompter panel
    d.rectangle([(0, 940), (1920, 1080)], fill=PANEL_COLOR)
    d.line([(0, 940), (1920, 940)], fill=LINE_COLOR, width=2)
    
    # Speaker badge
    d.rounded_rectangle([(50, 955), (320, 985)], radius=6, fill=(24, 32, 15), outline=(72, 93, 46))
    d.text((65, 962), f"🎙 {speaker}", fill=LIME, font=FONT_TAG)
    
    # Narration text with word wrapping
    words = narration_text.split(" ")
    lines = []
    curr = ""
    for w in words:
        if len(curr + " " + w) < 130:
            curr = curr + (" " if curr else "") + w
        else:
            lines.append(curr)
            curr = w
    if curr:
        lines.append(curr)
        
    y = 995
    for line in lines[:2]:
        d.text((65, y), line, fill=WHITE, font=FONT_NARRATION)
        y += 26

def draw_card(d, x, y, w, h, title=None, subtitle=None, border_color=LINE_COLOR, fill=CARD_BG):
    d.rounded_rectangle([(x, y), (x + w, y + h)], radius=12, fill=fill, outline=border_color, width=1)
    if title:
        d.text((x + 24, y + 20), title, fill=WHITE, font=FONT_BODY_BOLD)
    if subtitle:
        d.text((x + 24, y + 46), subtitle, fill=MUTED, font=FONT_TAG)
        d.line([(x + 24, y + 70), (x + w - 24, y + 70)], fill=LINE_COLOR, width=1)

print("Helper functions initialized successfully.")
