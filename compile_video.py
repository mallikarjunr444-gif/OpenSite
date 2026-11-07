import os
import math
import struct
import wave
import subprocess

BASE_DIR = "/Users/malikarjunr/hack"
ASSETS_DIR = os.path.join(BASE_DIR, "video_assets")
FRAMES_DIR = os.path.join(ASSETS_DIR, "frames")
FINAL_VIDEO = os.path.join(BASE_DIR, "OpenSite_Demo_Video.mp4")

# Scene durations matching the 4-5 minute script
scene_durations = [
    ("frame_01.png", 15),  # Scene 1: 0:00 - 0:15 Intro
    ("frame_02.png", 15),  # Scene 1: 0:15 - 0:30 Purpose & Live Overview
    ("frame_03.png", 22),  # Scene 2: 0:30 - 0:52 4 Growth Bottlenecks
    ("frame_04.png", 23),  # Scene 2: 0:52 - 1:15 Core AI Agent Question
    ("frame_05.png", 15),  # Scene 3: 1:15 - 1:30 Unified Architecture
    ("frame_06.png", 15),  # Scene 3: 1:30 - 1:45 Persistent Intelligence Differentiator
    ("frame_07.png", 20),  # Scene 4: 1:45 - 2:05 12 Core Capabilities Matrix
    ("frame_08.png", 20),  # Scene 4: 2:05 - 2:25 Technical Audit & Search Console
    ("frame_09.png", 20),  # Scene 4: 2:25 - 2:45 Conversion & Experiment Intelligence
    ("frame_10.png", 15),  # Scene 5: 2:45 - 3:00 Hindsight Architecture
    ("frame_11.png", 22),  # Scene 5: 3:00 - 3:22 Live Demo: Retain Operation
    ("frame_12.png", 23),  # Scene 5: 3:22 - 3:45 Live Demo: Recall Operation
    ("frame_13.png", 15),  # Scene 5: 3:40 - 3:45 Why Memory Changes Everything
    ("frame_14.png", 20),  # Scene 6: 3:45 - 4:05 Long-Term Growth Journey
    ("frame_15.png", 15),  # Scene 6: 4:05 - 4:20 Closed-Loop AI Advisor Vision
    ("frame_16.png", 15),  # Scene 7: 4:20 - 4:35 Understand. Optimize. Grow.
    ("frame_17.png", 13)   # Scene 7: 4:35 - 4:48 Credits & Project Showcase
]

total_seconds = sum(dur for _, dur in scene_durations)
print(f"Total video duration: {total_seconds} seconds ({total_seconds//60}m {total_seconds%60}s)")

# Synthesize keynote ambient soundtrack
AUDIO_PATH = os.path.join(ASSETS_DIR, "ambient_soundtrack.wav")
SAMPLE_RATE = 44100
total_samples = int(total_seconds * SAMPLE_RATE)

chords = [
    [146.83, 220.00, 261.63, 329.63, 440.00],  # Dm9
    [116.54, 174.61, 233.08, 293.66, 349.23],  # Bbmaj7
    [174.61, 220.00, 261.63, 349.23, 440.00],  # Fmaj7
    [130.81, 196.00, 246.94, 293.66, 392.00]   # C9
]
chord_dur = 6.0

print("Synthesizing ambient presentation audio...")
with wave.open(AUDIO_PATH, "w") as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(SAMPLE_RATE)
    buf = bytearray()
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        chord_idx = int((t / chord_dur) % len(chords))
        current_chord = chords[chord_idx]
        val_l, val_r = 0.0, 0.0
        for f_idx, freq in enumerate(current_chord):
            amp = 0.07 / (f_idx + 1)
            mod = 1.0 + 0.15 * math.sin(2 * math.pi * 0.4 * t)
            pan = 0.5 + 0.3 * math.sin(0.2 * t + f_idx)
            wv = math.sin(2 * math.pi * freq * t) * amp * mod
            val_l += wv * (1.0 - pan)
            val_r += wv * pan
        arp_note = current_chord[int((t * 2.0) % len(current_chord))] * 2.0
        arp_decay = math.exp(-6.0 * (t % 0.75))
        arp_val = math.sin(2 * math.pi * arp_note * t) * 0.035 * arp_decay
        val_l += arp_val * 0.4
        val_r += arp_val * 0.6
        fade = 1.0
        if t < 2.0: fade = t / 2.0
        elif t > (total_seconds - 3.0): fade = (total_seconds - t) / 3.0
        l_sample = int(max(-32767, min(32767, val_l * fade * 32767)))
        r_sample = int(max(-32767, min(32767, val_r * fade * 32767)))
        buf.extend(struct.pack("<hh", l_sample, r_sample))
        if len(buf) >= 32768:
            wav_file.writeframes(buf)
            buf = bytearray()
    if buf: wav_file.writeframes(buf)
print("Audio synthesized:", AUDIO_PATH)

CONCAT_FILE = os.path.join(ASSETS_DIR, "concat_list.txt")
with open(CONCAT_FILE, "w") as f:
    for fname, dur in scene_durations:
        f.write(f"file '{os.path.join(FRAMES_DIR, fname)}'\n")
        f.write(f"duration {dur}\n")
    f.write(f"file '{os.path.join(FRAMES_DIR, scene_durations[-1][0])}'\n")

print("Encoding final MP4 video via ffmpeg...")
cmd = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", CONCAT_FILE,
    "-i", AUDIO_PATH,
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    FINAL_VIDEO
]
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if res.returncode == 0:
    sz = os.path.getsize(FINAL_VIDEO) / (1024 * 1024)
    print(f"SUCCESS: Video generated at {FINAL_VIDEO} ({sz:.2f} MB, {total_seconds}s)")
else:
    print("FFmpeg error:", res.stderr[-500:])
