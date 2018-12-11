import face_recog
import os, sys
import sender
import email_sender

def main(name, email):
	os.system("sudo modprobe bcm2835-v4l2")
	arg = "python3 face_recog.py -n 2 -a " + name
	#os.system(arg)
	sender.initialize(name)
	email_sender.send_email(email)
	
	
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])