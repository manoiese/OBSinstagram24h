@echo off
:reinicio
python live_broadcast_ffmpeg.py -u usuarioinstagram -p senhainstagram -f C:\WEBSERVER\root\stream\live.m3u8
goto reinicio
exit
