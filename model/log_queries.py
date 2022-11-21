from os import getcwd

path = getcwd()[:-4]

def clear_logs():
	f = open("{}lqueries.log".format(path), "w+").close()

def write_to_log(text, filename="{}lqueries.log".format(path)):
	with open(filename, "a+") as f:
		f.write(text + "\n")
		f.close()