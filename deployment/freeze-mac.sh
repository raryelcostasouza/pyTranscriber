#!/bin/bash

pipenv shell
pyinstaller main.py \
--path="$(pwd)" \
--add-binary="ffmpeg:." \
--add-binary="pytranscriber.sqlite:." \
--add-data="pytranscriber/gui/*.qm:pytranscriber/gui/" \
--add-data="venv/lib/python3.8/site-packages/whisper/assets:whisper/assets" \
--clean  \
--windowed \
--noconfirm \
--clean \
#--osx-entitlements-file="mac/entitlements.plist"