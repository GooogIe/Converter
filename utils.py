#!/usr/bin/python
# -*- coding: utf-8 -*-

#Imports
import os
import sys

#Don't create .pyc
sys.dont_write_bytecode = True

#Colours
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
defcol = "\033[0m"

all_files = ['bmp','jpg','png','jpeg','wma','m4p','au','aac','mp4','flv','wav','mp3','ogg','flac','flic','3gp','ac3','f4v','ffm','m4v''mov','mlv','m4a','mp2']

#Output functions
def logaction(text):
	print red+"["+blue+"#"+red+"] - "+defcol+text

def action(text):
	print red+"["+green+"+"+red+"] - "+defcol+text

def action2(text):
	print(red+"["+green+"+"+red+"] - "+"\n"+defcol+text)

def alert(text):
	print red+"["+yellow+"!"+red+"] - "+defcol+text

def error(text):
	print red+"["+yellow+"!"+red+"] - "+defcol+text
	sys.exit()

def input(text):
	return raw_input(red+"["+blue+"#"+red+"] - "+defcol+text)

#Check mp3gain installation
def mp3gain():
	mp3gain = "/usr/bin/mp3gain"
	if os.path.isfile(mp3gain):
		return True
	else:
		error("Couldn't find a valid mp3gain installation, install it via sudo apt-get install mp3gain  if you are on a debian based distribution or via sudo yum install mp3gain if you are on fedora based distribution.")
		return False

#Check ffmpeg installation
def ffmpeg():
	ffmpeg = "/usr/bin/ffmpeg"
	if os.path.isfile(ffmpeg):
		return True
	else:
		error("Couldn't find a valid ffmpeg installation, install it via sudo apt-get install ffmpeg if you are on a debian based distribution or via sudo yum install ffmpeg if you are on a fedora based distribution.")
		return False

def init():
	logaction("This is a little python script which converts any file whose format is accepted by ffmpeg (also mp4, mov...) into a desired format, keeping metadatas, editing bitrate, audio channels, and you also can normalize files' volume.")

	logaction("This script uses "+red+"ffmpeg"+defcol+" for the conversion and "+green+"mp3gain"+defcol+" for the normalization.")
#Replace any special character with \ and the character
def cleanstr(f):
	f = f.replace(" ","\ ",100)
	f = f.replace(",","\,",100)
	f = f.replace("'","\\'",100)
	f = f.replace('"','\\"',100)
	f = f.replace("(","\(",100)
	f = f.replace(")","\)",100)
	f = f.replace("[","\[",100)
	f = f.replace("]","\]",100)
	f = f.replace("@","\@",100)
	f = f.replace("#","\#",100)
	f = f.replace("è","\è",100)
	f = f.replace("ù","\ù",100)
	f = f.replace("&","\&",100)
	f = f.replace("-","\-",100)
	f = f.replace(".","\.",100)
	return f



def getfileext(infile):
	fext = infile.split(".")
	return fext[len(fext)-1]

def alreadyConverted(indir,outdir,outform): #Return the number of already converted files in the output directory, if not empty
	infiles = [os.path.join(root, name) for root, dirs, files in os.walk(os.getcwd()+"/"+indir) for name in files if name.endswith(tuple(all_files))] #http://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
	outfiles = [os.path.join(root, name) for root, dirs, files in os.walk(os.getcwd()+"/"+outdir) for name in files if name.endswith(tuple(all_files))] #http://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python
	infiles.sort()
	outfiles.sort()
	if len(outfiles) == 0:
		return -1
	else:
		newfiles = []
		exist = False
		for ifile in infiles:
			ifile = ifile.replace(getfileext(ifile),outform,1)
			for ofile in outfiles:
				if ifile.replace(os.getcwd()+"/"+indir,"",1)== ofile.replace(os.getcwd()+"/"+outdir,"",1):
					exist = True
			if exist == False:
				newfiles.append(ifile)
			else:
				exist = False
		newfiles.append(len(newfiles))
		return newfiles


#Obtain directory size in mbyte
def getdirsize(path):
    	total_size = 0
   	for dirpath, dirnames, filenames in os.walk(path):
       		for f in filenames:
			if f.endswith(tuple(all_files)):
        			fp = os.path.join(dirpath, f)
        			total_size += os.path.getsize(fp)
    	return total_size/1024/1024
