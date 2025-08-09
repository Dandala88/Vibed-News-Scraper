[app]

# Application details
title = News Agent Mobile
package.name = newsagent
package.domain = com.newsagent.mobile

# Source details
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
source.exclude_dirs = tests, bin, venv, __pycache__, .git
source.exclude_patterns = license,images/*/*.jpg

# Version
version = 1.0

# Application requirements
requirements = python3,kivy,kivymd,requests,beautifulsoup4,feedparser,textstat,lxml,certifi,charset_normalizer,idna,urllib3,soupsieve,typing_extensions,pyphen,cmudict,setuptools

# Android specific
[android]
api = 31
minapi = 21
ndk = 25b
sdk = 31
permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE
archs = arm64-v8a, armeabi-v7a

# Icon and presplash
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Orientation
orientation = portrait

# Services
[services]
# No background services needed

# Build configuration
[buildozer]
log_level = 2
warn_on_root = 1