import os
from dotenv import load_dotenv


load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "192.168.0.100")
SERVER_LOCAL_IP = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 4096
SEP1 = "<SEP1>"
SEP2 = "<SEP2>"