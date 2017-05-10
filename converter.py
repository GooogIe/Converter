#!/usr/bin/python
# -*- coding: utf-8 -*-

#Imports
import os
import argparse
import utils
import timeit
import datetime

#Allowed extensions
all_files = ['bmp','jpg','png','jpeg','wma','m4p','au','aac','mp4','flv','wav','mp3','ogg','flac','flic','3gp','ac3','f4v','ffm','m4v''mov','mlv','m4a','mp2']

convertable = ['wma','m4p','au','aac','mp4','flv','wav','mp3','ogg','flac','flic','3gp','ac3','f4v','ffm','m4v''mov','mlv','m4a','mp2']

#Conversion speed: Approx 2 sec/mb (Depend on threads and PC specs)
cspeed = 2

#Converter's class
class Converter:
	#Converter's class constructor method
	def __init__(self,toconvert,outformat,inputdir,outputdir,threads = 1,channels = 2,bitrate = 128,normalize = False,decibel = 1.0,verbosity = False):
		self.toconvert = toconvert
		self.outformat = outformat
		self.inputdir = inputdir
		self.outputdir = outputdir
		self.threads = threads
		self.channels = channels
		self.bitrate =bitrate
		self.normalize = normalize
		self.decibel = decibel
		self.verbosity = verbosity

	def getSettings(self):
		utils.logaction("Input Directory: "+self.inputdir)
		utils.logaction("Output Directory: "+self.outputdir)
		utils.logaction("Output Format: "+self.outformat)
		utils.logaction("Threads: "+str(self.threads))
		utils.logaction("Channels: "+str(self.channels))
		utils.logaction("Bitrate: "+str(self.bitrate))
		utils.logaction("Normalize: "+str(self.normalize))
	#Create subdirectory for files during conversion
	def createsubdir(self,outfile):
		sd = outfile.replace(self.inputdir,self.outputdir+"/",1).split("/")#Split fdest in a list by the '/'
		subdir= '/'.join(sd[0:len(sd)-1])+"/"

		if os.path.exists(subdir) == False:
 			os.system("mkdir " +subdir)


	#Get the file names with full path
	def getfilenames(self,infile):
		outfile = infile.replace(self.inputdir,self.outputdir+"/",1) #Replace source directory in the output file name
		fileext =utils.getfileext(outfile)
		if fileext in convertable:
			outfile = outfile.replace(fileext,self.outformat,1)
			toprint = "Converting "+infile.replace(os.getcwd(),"",1)
		else:
			toprint = "Copying "+infile.replace(os.getcwd(),"",1)

		outfile = utils.cleanstr(outfile) #Add \ for special characters
		infile = utils.cleanstr(infile)
		return [infile,outfile,toprint]

	#Convert method
	def convert(self):
		converted = 0
		total = len(self.toconvert)
		for infile in self.toconvert:
			fnames = self.getfilenames(infile)
			infile = fnames[0]
			outfile = fnames[1]
			out = fnames[2]
			print outfile
			self.createsubdir(outfile)
			if utils.getfileext(infile) in convertable:
				if self.verbosity == False:
					utils.action(out)
					os.system("ffmpeg -vsync 2 -y -threads "+str(self.threads)+" -ac "+str(self.channels)+" -i "+infile+" -b:a "+str(self.bitrate)+"k -bufsize "+str(self.bitrate)+"k "+outfile+ " >/dev/null 2>&1")
				else:
					os.system("ffmpeg -vsync 2 -y -threads "+str(self.threads)+" -ac "+str(self.channels)+" -i "+infile+" -b:a "+str(self.bitrate)+"k -bufsize "+str(self.bitrate)+"k "+outfile)
				converted += 1
			else:
				utils.action(out)
				os.system("cp "+infile+" "+outfile)
				converted +=1
		return converted

	def normalize(self):
		tonormalize = [os.path.join(root, name) for root, dirs, files in os.walk(os.getcwd()+"/"+self.outputdir) for name in files if name.endswith(tuple(convertable))]
		i = 0
		for f in tonormalize:
			f = utils.cleanstr(f)
			tonormalize[i] = f
			i +=1
		utils.action("Normalizing files.")
		try:
			if self.verbosity == False:
				os.system("mp3gain -k -r -d "+str(self.decibel)+" "+" ".join(tonormalize)+ " >/dev/null 2>&1")
			else:
				os.system("mp3gain -k -r -d "+str(self.decibel)+" "+" ".join(tonormalize))
		except:
			utils.alert("Error during normalizing files.")

# ----------------  Main ---------------------
def main():

	#Arg parser
	parser = argparse.ArgumentParser(description='This is a little python script which converts any file whose format is accepted by ffmpeg ( also mp4, mov... ) into a desired format, keeping metadatas, editing bitrate, audio channels, and even normalizing them using mp3gain.')
	parser.add_argument('-i','--input',nargs='+',metavar='My Music',type = str, help='Input directory name ( No / ).',required=True)
	parser.add_argument('-o','--output',nargs='+',metavar='My Converted Music',type = str,help='Output directory name ( No / ).', required=True)
	parser.add_argument('-f','--format',metavar='mp3',type = str,help="Output file format (mp3,flac,wav ... ) .",required=True)
	parser.add_argument('-b','--bitrate',metavar='320',type = int,help="Change the bitrate of the output file (128kbps by default ).", required=False)
	parser.add_argument('-c','--channels',metavar='2',type = int,help="Output audio channels (Stereo by default).",required=False)
	parser.add_argument('-t','--threads',metavar='10',type = int,help="Set number of thread to use while converting a file, be careful with this setting, it's suggested not to use higher value than 10 (1 By default ) .",required=False)
	parser.add_argument('-d','--decibel',metavar='1.0',help="Modify suggested dB gain of the normalization ( Works only if normalization is enabled, 1.0 by default ).",required=False)
	parser.add_argument('-n','--normalize',help="Enable normalization of converted files using mp3gain ( Disabled by default ).", action='store_true',required=False)
	parser.add_argument('-v','--verbosity',help="Increase verbosity if toggled, show ffmpeg and mp3gain commands output ( Disabled by default ).", action='store_true',required=False)
	args = parser.parse_args()


	#Load args into variables
	inputdir = ' '.join(args.input)
	outputdir = ' '.join(args.output)
	outformat = args.format

	#Check if non required args are not empty, and if yes set a default value
	if args.bitrate != None:
		bitrate = args.bitrate
	else:
		bitrate = "128"

	if args.verbosity != None:
		verbosity = args.verbosity
	else:
		verbosity = False

	if args.threads != None:
		threads = args.threads
	else:
		threads = "1"

	if args.channels != None:
		channels = args.channels
	else:
		channels  = "2"

	if args.normalize != None:
		normalize = args.normalize
	else:
		normalize =False

	if args.decibel != None:
		decibel = float(args.decibel)
	else:
		decibel = 1.0


	utils.init()
	if normalize == True:
		if utils.mp3gain() == False:
			utils.alert("In order to normalize your files you need to install mp3gain.")
			return
	if utils.ffmpeg() == False:
		return

	#Check if input directory exists
	if not os.path.exists(inputdir):
 		utils.alert("Input directory doesn't exist, quitting...")
		return

	#If the directory doesn't exist create it
	if not os.path.exists(outputdir):
 	   	 os.system("mkdir "+utils.cleanstr(outputdir))

	#Load files to be converted in a list
	toconvert = [os.path.join(root, name) for root, dirs, files in os.walk(os.getcwd()+"/"+inputdir) for name in files if name.endswith(tuple(all_files))] #http://stackoverflow.com/questions/5817209/browse-files-and-subfolders-in-python

	#Load the new files to be converted in a list
	new = utils.alreadyConverted(inputdir,outputdir,outformat)

	mans = ''
	if new != -1:
		while mans != 'no' and mans != 'yes' and mans!= 'y' and mans!= 'n':
			mans = utils.input("Found "+str(len(new)-1)+" new files to be converted. Would you like to convert only the new ones?(y/n): ")
		if mans == 'y' or mans == 'yes':
			new.pop()
			toconvert = new

	#Create Converter instance
	MyConverter = Converter(toconvert,outformat,inputdir,outputdir,threads,channels,bitrate,normalize,decibel,verbosity)

	utils.action(str(len(toconvert))+" files loaded.")
	utils.action("Size of files to be converted: "+str(utils.getdirsize(inputdir))+" MB.")
	utils.action("Estimated conversion time (normalization not included): "+str(utils.getdirsize(inputdir)*cspeed/60)/self.threads+" minutes.")
	MyConverter.getSettings()
	ans = ''
	while ans != 'no' and ans != 'yes' and ans!= 'y' and ans!= 'n':
		ans = utils.input("These are your settings, would you like to continue?(y/n): ")
		if ans == 'no' or ans == 'n':
			utils.action("Quitting.")
			return

	start_time = timeit.default_timer()
	try:
		conv = MyConverter.convert()
	except KeyboardInterrupt:
		return

	if normalize == True:
		MyConverter.normalize()
	elapsed = timeit.default_timer() - start_time

	utils.action("Converted "+str(conv)+ "/"+ str(len(toconvert))+" files in "+str(int(elapsed)/60)+" minutes.")
if __name__ == "__main__":
	main()
