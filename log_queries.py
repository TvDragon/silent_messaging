def clear_logs():
	f = open("lqueries.log", "w+").close()

def write_to_log(text, filename="lqueries.log"):
	with open(filename, "a+") as f:
		f.write(text + "\n")
		f.close()
