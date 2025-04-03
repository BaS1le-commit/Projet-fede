from pynput import keyboard
from src.drone_command import DroneCommand
from src.flaskAPI import main_api
import subprocess, sys, os
import time

class ClavierController:
    def __init__(self, app_ref):
        self.drone = DroneCommand()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.app_ref = app_ref
        self.SPEED = 50

    def on_press(self, key):
        try:
            if key.char == 'z':
                self.drone.move(fb=self.SPEED)
            elif key.char == 's':
                self.drone.move(fb=-self.SPEED)
            elif key.char == 'q':
                self.drone.move(lr=-self.SPEED)
            elif key.char == 'd':
                self.drone.move(lr=self.SPEED)
            elif key.char == 'j':
                self.drone.move(ud=self.SPEED)
            elif key.char == 'n':
                self.drone.move(ud=-self.SPEED)
            elif key.char == 'a':
                self.drone.move(yaw=-self.SPEED)
            elif key.char == 'e':
                self.drone.move(yaw=self.SPEED)
            elif key.char == 't':
                self.drone.takeoff()
            elif key.char == 'l':
                self.drone.land()
            elif key.char == 'k':
                self.drone.land() 
                time.sleep(3)
                self.app_ref.cleanup()
                subprocess.run(["bash", "start_api.sh"])
        
        except AttributeError:
            pass

    def on_release(self, key):
        if key == keyboard.Key.esc:
            print("Arrêt d'urgence")
            self.drone.land()
            return False
        else:
            self.drone.stop()
