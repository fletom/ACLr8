#!/usr/bin/env sudo python -u

import re
import subprocess
from sys import stdout, platform


write = stdout.write

try:
	write("\nWelcome to ACLr8 version 1.4.\n")
	write("Press Ctrl-C to stop the program at any time.\n\n")
	
	if platform != 'darwin':
		write("Sorry, this script only works on Mac OS X.\n")
		exit(-1)
	
	write("Reading permission errors (this can take a very long time)... ")
	process = subprocess.Popen(
		['diskutil', 'verifyPermissions', '/'],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		universal_newlines = True, # makes .communicate() return strings instead of bytes on 3.x
	)
	stdoutdata, stderrdata = process.communicate()
	write("done.\n")
	if process.returncode:
		write("\nReading permission errors failed with error: \"%s\"\n" % stderrdata.strip())
		exit(-1)
	
	files = []
	regex = re.compile('^ACL found but not expected on "(.*)"\.?$')
	for line in stdoutdata.split('\n'):
		line = line.strip()
		match = regex.search(line)
		
		if match is not None:
			file_path = match.group(1)
			file_path = '/' + file_path # diskutil omits the leading slash
			files.append(file_path)
	
	write("Found %d files with unexpected ACL.\n" % len(files))
	
	if files:
		write("Removing ACL from all files... \n")
		for file_path in files:
			process = subprocess.Popen(['chmod', '-h', '-N', file_path], stderr = subprocess.PIPE, universal_newlines = True)
			stdoutdata, stderrdata = process.communicate()
			if process.returncode:
				write("\nRemoving ACL from \"%s\" failed with error: \"%s\"\n" % (file_path, stderrdata.strip()))
	
	write("\nFinished!\n")
except KeyboardInterrupt:
	write("\nYou have manually terminated the program.\n")
except Exception:
	write("\nAn unexpected error occurred. Please submit the following traceback as a bug report:\n\n")
	raise
