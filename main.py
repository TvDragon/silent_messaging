from os import getcwd
import sys
from client import Client

path = getcwd()
sys.path.insert(0, "{}/view/".format(path))

from window import *

def main():
	user_client = Client()
	start_app(user_client)

if __name__ == "__main__":
	main()