@echo off
:reinicio
python live_broadcast_ffmpeg.py -u riovermelhofm -p rvermelho967 -f C:\WEBSERVER\root\stream\live.m3u8
goto reinicio
exit
