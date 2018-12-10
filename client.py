from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
import paramiko

DEVICE_IP = "155.41.93.194"

def client():
	global root
	root = Tk()
	style = ttk.Style()
	style.configure("Title.TLabel", font=('calibri', '18', 'bold'))
	style.configure("Data.TLabel", font=('calibri', '12'))

	root.title('SmartDoor Client')
	root.geometry('725x400')

	MainWindow(root).pack()
	root.mainloop()

"""
GUI Window - capture credentials and call add_user()
"""
class MainWindow(Frame):
	def __init__(self, root):
		Frame.__init__(self, root)
		root.configure(bg = 'gray92')

		# title
		self.file_label = Label(self, text='Add New User', style='Title.TLabel')
		self.file_label.grid(row=4, column=0, sticky=E, pady=7)

		# enter name
		self.name_label = Label(self, text='Enter User Name', style='Data.TLabel').grid(row=5, column=1, sticky=W, pady=7)
		self.name = Entry(self)
		self.name.grid(row=5, column=2, sticky=N, pady=7)

		# enter password
		self.passwd_label = Label(self, text='Enter Server Password', style='Data.TLabel').grid(row=6, column=1, sticky=W, pady=7)
		self.passwd = Entry(self, show="*")
		self.passwd.grid(row=6, column=2, sticky=N, pady=7)

		# submit button
		self.train = Button(self, text='Add User', width=10, command=lambda:self.add_user())
		self.train.grid(row=7, column=1, sticky=N, pady=7)

		Grid.rowconfigure(self, 0, weight=1)
		Grid.columnconfigure(self, 1, weight=1)

	"""
	Use the parmiko module to open an ssh connection with the remote device
	Once connection is made, pass variables from GUI widgets into shell command
	"""
	# TODO handle spaces in name
	def add_user(self):
		user_name = self.name.get()
		ssh_passwd = self.passwd.get()

		ssh_client = paramiko.SSHClient()
		ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

		try:
			ssh_client.connect(DEVICE_IP, username='pi', password=ssh_passwd)
		except:
			print("wrong password\n")

		for command in 'cd Documents/SmartDoor && python test_ssh.py {}'.format(user_name), 'uname', 'uptime':
			stdin, stdout, stderr = ssh_client.exec_command(command)
			stdin.close()
			print(repr(stdout.read()))
			stdout.close()
			stderr.close()
		ssh_client.close


if __name__ == '__main__':
	client()