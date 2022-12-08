import json
from os.path import exists

def create_msg_file(user):
	
	filename = "{}.json".format(user["username"])
	if not exists(filename):
		contents = {
			"messages": []
		}
		f = open(filename, "w")
		contents = json.dumps(contents, indent=4)
		f.write(contents)
		f.close()