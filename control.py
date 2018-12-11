import face_recog
import os, sys

def main(name):
	arg = "python3 face_recog.py -n 2 -a " + name
	os.system(arg)
	
	
	
	
if __name__ == '__main__':
	main(sys.argv[1])