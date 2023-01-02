# Messaging Application

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
<ol>
  <li>
    <a href="#about-the-project">About The Project</a>
    <ul>
      <li><a href="#built-with">Built With</a></li>
    </ul>
  </li>
  <li>
    <a href="#getting-started">Getting Started</a>
    <ul>
      <li><a href="#prerequisites">Prerequisites</a></li>
      <li><a href="#installation">Installation</a></li>
    </ul>
  </li>
  <li><a href="#usage">Usage</a></li>
</ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Originally, this was supposed to be an ecrypted messaging application where the messages would be encrypted before being send over the server however, I ran into issues trying to convert the encrypted messages into a string so I had to remove that from this project. Although, this is something that I'd like to work back on in the near future. This project is a messaging application on the desktop like other social messaging applications like skype and discord however, the messages would be stored on the users PC instead of on a server permanently. This was made as I wanted to learn how users were able to message someone over the internet using sockets and also used some knowledge on multithreading which I took a course in during university to create this application. It is noted that messages are stored temporarily on the server but the messages will be deleted once the receiver has logged on to retrieve those messages.

### Build With

* [![Python][python]][Python-url]

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

### Installation

1. Clone this repository to your desired location using git or download the zip file and extract it.

2. You will be required to have python install and the following python library dependencies listed below. Follow the steps to install python from this [website](https://realpython.com/installing-python/). You'll need to set up a virtual environment as well which you can follow from the virtualenv dependency.

	* [virtualenv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
	* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/)

<!-- USAGE EXAMPLES -->
## Usage

1. Once you have performed the installation listed in the previous steps. Open up a terminal or command prompt and enter the command below to enter your virtual environment. The name of your folder like "env" will be what you named it when setting up the virtual environment.

		source env/bin/activate

2. There will be a server and client version in their respective folders. The server version handles client connections and the client is the user. If you wish to run the server and/or client version run the commands below respectively.

		python server/server.py
		python client/main.py

3. If you wish to deactive your virtual environment run the command below.

		deactivate

<!-- Example -->
## Application Demonstration

## Example Models

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[python]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[Python-url]: https://www.python.org/