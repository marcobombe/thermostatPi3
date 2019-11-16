#!/usr/bin/env python
"""This is a simple python script to control mpg321 or mpg123. Since mpg123
is not free software and you cannot use it in your own projects easily,
it is recommended that you use mpg321, which is available under the GPL.

Basic primer for use:

	foo = mpg321.mpg321()              # Instaneate an mpg321 object
	foo.load('some_random_file.mp3')   # This will load and play the mp3
	foo.process_forever()              # Process mpg321 status messages
	                                   # until the end of the song.

You can also make your own loop and call the process_once() method. Be 
warned that if you don't call process_once() often enough, playback will 
stop. Practical experiance shows that aproximately 7 seconds of audio will 
play if you don't ever call process_once(), and gets shorter at higher 
bitrates.

Various things you may set:

	debug		Debugging information. Higher numbers get you more
	mpg321		The name of your mpg321/mpg123 binary
"""

COPYRIGHT = """COPYRIGHT (C) 2001 Zachary White <zwhite@darkstar.frop.org>
Permission to use, copy, modify, and distribute this software and
its documentation for any purpose and without fee is hereby granted,
provided that the above copyright notice appear in all copies and
that both that copyright notice and this permission notice appear in
supporting documentation.

THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
VERSION = '0.8'

class mpg321:
	"""A class to control an instance of mpg321.

	When an mpg321 object has been instantiated, it can be used to play
	specified mp3s.
	"""

	# Modules I use
	import os, string, re

	# Variables
	nowplaying = ''
	mpg321 = 'mpg123'
	options = ''

	# These correspond to @S' output.
	fileversion = 1.0
	filelayer = 0
	samplerate = 0
	stereo_mode = ''
	mode_extention = 0
	bytes_frame = 0
	audio_channels = 0
	copyrightflag = 0
	emphasis = 0
	bitrate = 0
	extention = 0

	# These correspond to @F's output
	current_frame = 0
	frames_remaining = 0
	current_time = 0
	time_remaining = 0

	# This is always what the last @P message we recieved is
	playstatus = 0

	# Do we want debugging output? The higher the number the more output.
	# 0 = no debugging information
	# 1 = print the song name when loading
	# 2 = print a message when certain commands are run
	# 3 = Show every status message from mpg321
	debug = 0

	def load(self, file):
		"""Load and play the specified file"""
		if self.os.path.isfile(file):
			if self.debug:
				print 'mpg321.py: DEBUG: Loading %s' % file
			self.processin.write('LOAD %s\n' % file)
			self.process_once()
			self.process_once()
		else:
			if self.debug:
				print 'mpg321.py: DEBUG: Unable to load %s' % file
			raise 'File error'

	def jump(self, frame):
		"""Jumps to the specified frame number, or jumps the specified
		number of frames forwards or backwards.

		If you specify an absolute integer for frame, you will jump
		to that specific frame.

		If you specify +n or -n, playback will jump forwards or 
		backwards n frames.
		"""
		self.processin.write('JUMP %s\n' % frame)
		if self.debug > 1:
			print 'mpg321.py: DEBUG: Jump command: %s' % frame

	def pause(self):
		"""Pauses or unpauses playback"""
		self.processin.write('PAUSE\n')
		if self.debug > 1:
			print 'mpg321.py: DEBUG: Paused music'

	def stop(self):
		"""Stops the current mp3."""
		if self.playstatus == 2:
			self.pause()
		self.jump('0')
		self.playstatus = 0

	def quit(self):
		"""Terminates the mpg321 process, and deletes self. Sets
		self.playstatus to -1 to indicate that the process has ended."""
		self.processin.write('QUIT\n')
		if self.debug > 1:
			print 'mpg321.py: DEBUG: Deleting self'
		self.playstatus = -1

	def status(self):
		"""Displays the current status of the player. Returns a tuple
		with the following structure:

		( status, arguments )

		Where status is one of 'play', 'pause', 'stop' and arguments
		depends on the status.

		Arguments:

			Play and pause return a tuple of the following form:

			( current_song, current_frame, frames_remaining, 
				current_time, time_remaining )

			Stop returns None.
		"""
	
		status = 'stop'
		arguments = None

		if self.playstatus == 1:
			status = 'pause'
		elif self.playstatus == 2:
			status = 'play'

		if self.debug > 1:
			print 'mpg321.py: DEBUG: self.playstatus: %s' % self.playstatus

		if self.playstatus > 0:
			arguments = ( self.nowplaying, self.current_frame,
			        self.frames_remaining, self.current_time,
        			self.time_remaining )

		return ( status, arguments )

	def __init__(self):
		"""Start the mpg321 process"""
		self.processin, self.processout = \
			self.os.popen2(self.mpg321 + ' %s -R mp3d' % self.options, 't', 1)

		line = self.processout.readline()
		if not self.re.match(r'^@R MPG123.*', line):
			if self.debug:
				print 'mpg321.py: DEBUG: __init__: %s' % line
			raise 'Problem running mpg321'

	def process_once(self):
		"""Process one status line from mpg321."""
		line = self.processout.readline()[:-1]

		if self.debug > 2:
			print 'mpg321.py: DEBUG: process_once: %s' % line

		line = self.string.split(line)

		if line == []:
			#self.playstatus = -1
			print 'mpg321.py: DEBUG: Why did I get a blank line from mpg321?'
			pass
		elif line[0] == '@I':
			self.nowplaying = self.string.join(line[1:])
			self.playstatus = 2
		elif line[0] == '@P':
			self.playstatus = int(line[1])
			if self.debug > 1:
				print 'mpg321.py: process_once: line[0]: %s line[1]: %s' % (line[0], line[1])
				print 'mpg321.py: process_once: self.playstatus: %s' % self.playstatus
		elif line[0] == '@S':
			self.fileversion = line[1]
			self.filelayer = line[2]
			self.samplerate = line[3]
			self.stereo_mode = line[4]
			self.mode_extention = line[5]
			self.bytes_frame = line[6]
			self.audio_channels = line[7]
			self.copyrightflag = line[8]
			self.emphasis = line[9]
			self.bitrate = line[10]
			self.extention = line[11]
			self.playstatus = 1
		elif line[0] == '@F':
			self.current_frame = line[1]
			self.frames_remaining = line[2]
			self.current_time = line[3]
			self.time_remaining = line[4]
		else:
			print 'mpg321.py: Unknown command: %s' % self.string.join(line)

	def process_forever(self):
		"""Program loop to check our status and get commands"""
		while 1:
			self.process_once()
			if not self.playstatus:
				break

if __name__ == '__main__':
	import sys
	mp3 = mpg321()
	if len(sys.argv) > 1:
		for i in sys.argv[1:]:
			print 'Playing %s' % i
			mp3.load(i)
			x = 0
			while 1:
				mp3.process_once()
				if x == 10:
					print 'status: %s' % mp3.playstatus
				if mp3.playstatus == 0:
					break
		mp3.quit()
		sys.exit()
