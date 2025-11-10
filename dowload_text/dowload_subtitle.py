import yt_dlp
import re
import glob

# ▶️ Your YouTube link (t=7s is fine)
VIDEO_URL = input("Please enter your youtube url :")



# ⚙️ yt-dlp options: subs only (English), use auto if needed
ydl_opts = {
    "skip_download": True,
    "writesubtitles": True,
    "writeautomaticsub": True,   # use auto subs if manual not available
    "subtitleslangs": ["en"],    # change to ['vi'] etc. if you want
    "subtitlesformat": "vtt",
    "outtmpl": "temp.%(ext)s",   # temporary subtitle file
    "quiet": True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(VIDEO_URL, download=True)

# 🔎 Find the downloaded .vtt file
vtt_files = glob.glob("temp*.vtt")
if not vtt_files:
    print("❌ No subtitles downloaded (try another lang or ensure the video has subs).")
    raise SystemExit(1)

vtt_file = vtt_files[0]

# 🧼 Clean VTT → plain text (keep original lines; remove timestamps/tags)
clean_lines = []
time_cue = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}")
inline_ts = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")
tags = re.compile(r"</?c>|</?\w+(?: [^>]*)?>", re.IGNORECASE)  # <c>, <i>, <b>, etc.
# 🔹 Convert VTT → plain text (remove timestamps and metadata)
with open(vtt_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

cleaned = []
for line in lines:
    if re.match(r"^\d\d:\d\d:\d\d\.\d\d\d", line):  # skip timestamps
        continue
    if line.strip() == "" or line.startswith("WEBVTT"):
        continue
    line = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", line)
    line = re.sub(r"</?c>", "", line)
    cleaned.append(line.strip())

# ✅ remove repeated consecutive lines
deduped = []
prev = None
for l in cleaned:
    if l != prev:
        deduped.append(l)
    prev = l

# 🧾 Get video title from yt_dlp info and make a clean filename
title = info.get("title", "video")
safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)  # remove illegal filename chars
OUTPUT_FILE = f"dowload_text\subtitles\{safe_title}.txt"

# 💾 Save text file with title at the top
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(title + "\n" + "=" * len(title) + "\n\n")  # add title + underline
    f.write("\n".join(deduped))

print(f"✅ Subtitle saved as plain text: {OUTPUT_FILE}")
