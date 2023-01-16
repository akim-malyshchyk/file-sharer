from socket import socket
import tqdm
import os
from settings import SERVER_LOCAL_IP, PORT, BUFFER_SIZE, SEP1, SEP2
import atexit


class Receiver(socket):
    def __init__(self):
        super().__init__()
        self.files_info = []

        self.bind((SERVER_LOCAL_IP, PORT))
        self.listen(5)
        print(f"[*] Listening as {SERVER_LOCAL_IP}:{PORT}")
        atexit.register(self.close)

    def receive_file(self, client_socket, filename, filesize):
        progress = tqdm.tqdm(range(filesize),
                             f"Receiving {filename}",
                             unit="B",
                             unit_scale=True,
                             unit_divisor=1024)
        with open(f'received/{filename}', "wb") as f:
            batch_num = 0
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                batch_num += 1
                progress.update(len(bytes_read))

    def receive_files(self, client_socket):
        received = client_socket.recv(BUFFER_SIZE).decode()
        self.files_info = received.split(SEP2)
        for file_info in self.files_info:
            filename, filesize = file_info.split(SEP1)
            filename = os.path.basename(filename)
            filesize = int(filesize)
            self.receive_file(client_socket, filename, filesize)


def main():
    r = Receiver()
    while True:
        try:
            client_socket, address = r.accept()
            print(f"[+] {address} is connected.")
            r.receive_files(client_socket)
            client_socket.close()
            print(f"[+] {address} is disconnected.")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
