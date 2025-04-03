import socket
import time

class DroneCommand:
    def __init__(self, ip="192.168.10.1", port=8889):
        self.TELLO_IP = ip
        self.TELLO_PORT = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._init_connection()

    def _init_connection(self):
        self.send_command("command")
        self.send_command("streamon")
        time.sleep(2)
        print("Drone pret à recevoir des commandes")

    def send_command(self, command):
        try:
            self.sock.sendto(command.encode('utf-8'), (self.TELLO_IP, self.TELLO_PORT))
            print(f"Commande envoyee : {command}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Erreur lors de l'envoi de : {command}")
            print(e)

    def move(self, lr=0, fb=0, ud=0, yaw=0):
        self.send_command(f"rc {lr} {fb} {ud} {yaw}")

    def takeoff(self):
        self.send_command("takeoff")

    def land(self):
        self.send_command("land")

    def stop(self):
        self.send_command("rc 0 0 0 0")

