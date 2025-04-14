import time
import socket
from socket import *

class MessageBoardClient:
    #iniatialization: address from input and port 16111 (server address and port)
    def __init__(self, port=16111):
        while True:
            print("Enter host address:", end=" ")
            host = input().strip()
            try:
                gethostbyname(host)
                self.host = host
                break
            except error:
                print("Invalid host address. Please try again.")
        self.port = port
        self.socket = None
        self.BUFFER_SIZE = 1024 #max byte to receive at once
        self.SENDING_COOLDOWN = 0.1 #delay to prevent overwhelming server

    #establish TCP connection to server
    def connect(self):
        try:
            self.socket =  socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"client: Connection Error: {e}")
            return False

    def close(self): #to properly close socket
        try:
            if self.socket:
                self.socket.close()
                self.socket = None
                print("\nclient: Connection closed properly")
        except Exception as e:
            print(f"\nclient: Error during closing connection: {e}")

    def send(self, message):
        try:
            self.socket.send(message.encode())
            #encode cause a byte-like is needed instead of type str
            time.sleep(self.SENDING_COOLDOWN)
        except Exception as e:
            print(f"client: Error sending message: {e}")

    def receive_message(self): #for getting server's reply
        try:
            return self.socket.recv(self.BUFFER_SIZE).decode()
        except Exception as e:
            print(f"client: Error receiving message: {e}")
    
    def receive_all(self): #for GET all messages from server
        all_data = []
        while True:
            data = self.receive_message()
            if not data:
                break
            all_data.append(data)
            if(data.strip().endswith('#')):
                break
            time.sleep(self.SENDING_COOLDOWN)
        return '\n'.join(all_data)
    
    def run(self):
        if not self.connect():
            return

        try:
            while True:
                try:
                    print("client:", end=" ")
                    command = input().strip().upper()

                    if command == "POST":
                        try:
                            self.send("POST\n")
                            while True:
                                line = input()
                                self.send(line + "\n")
                                if line == "#":
                                    break
                            print("server: " + self.receive_message())
                        except KeyboardInterrupt:
                            print("\nclient: Post operation cancelled by user")
                            self.send("#\n")  # Send termination character to server
                            return
                        
                    elif command == "GET":
                        try:
                            self.send("GET\n")
                            response=self.receive_all()
                            for line in response.split('\n'):
                                if line.strip():
                                    print("server: " + line)

                        except KeyboardInterrupt:
                            print("\nclient: Get operation cancelled by user")
                            return
                        
                    elif command == "DELETE":
                        try:
                            self.send("DELETE \n")
                            while True:
                                print("client:", end= " ")
                                line = input()
                                self.send(line + "\n")
                                if line == "#":
                                    break
                            print("server: " + self.receive_message())
                        
                        except KeyboardInterrupt:
                            print("\nclient: Delete operation cancelled by user")
                            self.send("#\n")  # Send termination character to server
                            return
                        
                    elif command == "QUIT":
                        try:
                            self.send("QUIT\n")
                            print("server: "+self.receive_message())
                        except Exception as e:
                            print(f"client: Error during quit: {e}")
                        break

                    else:
                        print("client: Invalid command. Available commands: POST, GET, DELETE, QUIT")

                except KeyboardInterrupt:
                    print("\nclient: Operation cancelled. Enter new command or QUIT to exit")
                    continue

        except KeyboardInterrupt:
            ("\nclient: Program interrupted by user. Closing connection...")
        finally:
            self.close()

if __name__ == "__main__":
    try:
        client = MessageBoardClient()
        client.run()
    except KeyboardInterrupt:
        print("\nclient: Program terminated by user before initialization")
    except Exception as e:
        print(f"client: Unexpected error occurred: {e}")





  



