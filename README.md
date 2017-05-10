# Converter

This is a little python script which converts any file whose format is accepted by ffmpeg (also mp4, mov...) into a desired format, keeping metadatas, editing bitrate, audio channels, and you also can normalize files' volume.

<p align="center"><img src="http://i.imgur.com/N3u3bIE.png" /</p>

Forgive me for any mistakes ( or just point me to the right way )  :>

This is a python script that allow you to:

* Convert any file whose format is allowed by ffmpeg into a desired one(must be supported by ffmpeg).
* Normalize your library's decibels (Customizable).
* A few more options c:

***

# Requirements #

* Python 2.7 or higher (not tested with 3 or higher, it may need some edits).
* ffmpeg installed on your machine more [here](https://ffmpeg.org/download.html).
* mp3gain installed, only if you want to normalize your library, more [here](http://mp3gain.sourceforge.net/)
* Brain.

# Usage #

* Clone this repository anywhere on your computer.
* Run 'python converter.py -h' to see all the available options.
* Example: 'python converter.py -i Music -o Converted Music -f mp3
  This will convert every file into the folder 'Music' into mp3, keeping directory trees, images, metadatas etc...
***

# Tips #

* Found a file supported by ffmpeg but the converter ignores it? Open converter.py and look for the 'convertable' list (convertable = ['wma',....]) insert here you extension.
* Use threads to convert you files quicker.
* Use 2 channels(as default), to get stereo output and not mono.
* Don't use too high bitrates, i think 192 or 256 it's enough for a good compromise of quality and size.

# More #

You can find me on:

* [Holeboards](www.holeboards.eu)
* [Telegram](www.telegram.me/eigoog)
