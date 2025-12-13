# drone_manager.py
from djitellopy import Tello
from typing import Dict
import time

class TelloDrone:
    """
    Clase Wrapper para manejar la comunicación con el Tello.
    """
    def __init__(self):
        self.drone = Tello()
        self.is_vertical_mode: bool = False
        self.rc_velocities: Dict[str, int] = {
            'lr': 0, 'fb': 0, 'ud': 0, 'yv': 0
        }

    def connect_and_setup(self) -> None:
        try:
            self.drone.connect()
            self.drone.streamon() 
            print(f"✅ Conectado. Batería: {self.get_battery_level()}%")
        except Exception as e:
            print(f"⚠️ Error de conexión: {e}")

    def get_battery_level(self) -> int:
        return self.drone.get_battery()

    def get_frame(self):
        return self.drone.get_frame_read().frame

    def takeoff(self) -> None:
        self.drone.takeoff()

    def land(self) -> None:
        self.drone.land()

    def flip(self, direction: str) -> None:
        """Direction: 'l', 'r', 'f', 'b'"""
        self.drone.flip(direction)

    def toggle_mode(self) -> None:
        self.is_vertical_mode = not self.is_vertical_mode
        mode_name = "VERTICAL/ROTACIÓN" if self.is_vertical_mode else "HORIZONTAL"
        print(f"🔄 Modo cambiado a: {mode_name}")

    def update_velocities(self, lr: int, fb: int, ud: int, yv: int) -> None:
        self.rc_velocities = {'lr': lr, 'fb': fb, 'ud': ud, 'yv': yv}

    def send_rc_command(self) -> None:
        # Envía los 4 canales
        self.drone.send_rc_control(
            self.rc_velocities['lr'],
            self.rc_velocities['fb'],
            self.rc_velocities['ud'],
            self.rc_velocities['yv']
        )

    def disconnect(self) -> None:
        self.drone.streamoff()
        self.drone.end()