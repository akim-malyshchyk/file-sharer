# File sharer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pylint](https://github.com/akim-malyshchyk/file-sharer/actions/workflows/pylint.yml/badge.svg)](https://github.com/akim-malyshchyk/file-sharer/actions/workflows/pylint.yml)

The app allows to simply transfer files from one machine to another via local network, at maximum allowed speeds.
The application was implemented using pure Python and sockets.

## Project structure
The project consists of two applications: `sender` and `receiver`. To transfer files, `gui.py` needs to be launched on sender machine, and `sock_receiver.py` needs to be launched on receiver machine side.
Sender part has GUI, receiver is implemented as command line module.

Both sender and receiver implemented as child classes of python `socket` class, which allows to utilize power of pure python sockets.

## Initial configuration
### Preparation
Before you start setting up the project, you need to install some PyGObject dependencies. You can check [here](https://pygobject.readthedocs.io/en/latest/getting_started.html) for detailed guide for your OS.

### Project setup
1. Cloning a repository with code
```
git clone https://github.com/akim-malyshchyk/file-sharer.git
```
2. Activating a virtual python environment and installing dependencies (inside the repository folder)
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
After that you should be able to launch `src/sender/gui.py` and `src/receiver/sock_receiver.py`

### How to use
That's how sender GUI and receiver CLI should look like if initial configuration went fine

<img src=https://github.com/akim-malyshchyk/file-sharer/assets/122870940/5565901a-0d60-44db-bf34-243ea49f59f1 height="300">
<img src=https://github.com/akim-malyshchyk/file-sharer/assets/122870940/0f03528f-d496-4c62-a488-cac5ab85e188 height="300">

After that everything is pretty simple:
1. Type your receiver machine local IP address
2. Choose file and click send

After that, receiver will create `received` folder and save the file there

<img src=https://github.com/akim-malyshchyk/file-sharer/assets/122870940/415436b4-7fa7-422a-82e1-70acfef3143e height="300">
<img src=https://github.com/akim-malyshchyk/file-sharer/assets/122870940/ec764261-cd05-4bd7-96ff-019b60afd7c8 height="300">
