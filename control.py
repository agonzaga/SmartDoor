import face_recog
import os, sys
import sender

def main(name, email):
	arg = "python3 face_recog.py -n 5 -a " + name
	os.system(arg)
	sender.initialize(name)
	
	
	
	
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])