import tqdm
from settings import BUFFER_SIZE
from socket import socket


class Sender(socket):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def send_bytes(self, file):
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            return False
        self.sendall(bytes_read)
        return True

    def send_file(self, filename, filesize):
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            result = True
            batch_index = 0
            while result:
                result = self.send_bytes(f)
                batch_index += 1
                progress.update(BUFFER_SIZE)
                yield (BUFFER_SIZE * batch_index) / filesize
