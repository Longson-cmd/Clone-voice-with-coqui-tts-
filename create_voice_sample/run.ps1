# .\run.ps1
ffmpeg -i my_file.mp3 -ss 00:03:00 -to 00:06:00 -c copy example.mp3
ffmpeg -i clip_3to6.mp3 -ar 22050 -ac 1 example.wav
# ffmpeg -i output_clone.wav -filter:a "atempo=0.9" output_clone_slow.wav
