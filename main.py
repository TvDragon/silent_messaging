from os import getcwd
import sys

path = getcwd()
sys.path.insert(0, "{}/view/".format(path))

from window import *

def main():
	start_app()

if __name__ == "__main__":
	main()