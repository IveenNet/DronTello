# drone_manager.py
import logging
import time
from typing import Dict

import numpy as np  # Necesario para crear la imagen negra
from djitellopy import Tello

import config


class TelloDrone:
    def __init__(self):
        self.drone = Tello()

        # --- 2. AÑADIR ESTO PARA SILENCIAR EL SPAM ---
        # Solo mostrará mensajes de ADVERTENCIA (Warning) o ERROR
        Tello.LOGGER.setLevel(logging.WARNING)
        # ---------------------------------------------

        self.is_vertical_mode: bool = False
        self.rc_velocities: Dict[str, int] = {
            'lr': 0, 'fb': 0, 'ud': 0, 'yv': 0
        }

    def connect_and_setup(self) -> None:
        """Establece conexión e inicia el stream de vídeo."""
        try:
            self.drone.connect()

            # Solo iniciamos vídeo si está habilitado en config
            if config.ENABLE_VIDEO:
                self.drone.streamon()
                print("⏳ Esperando estabilización del vídeo...")
                time.sleep(3)
            else:
                print("🚫 Vídeo DESACTIVADO por configuración (Modo Telemetría).")

            # Intentamos leer batería para confirmar conexión
            bat = self.get_battery_level()
            print(f"✅ Conectado. Batería: {bat}%")

        except Exception as e:
            print(f"⚠️ Error CRÍTICO de conexión: {e}")
            print("👉 SUGERENCIA: Revisa que estás conectado al Wi-Fi 'TELLO-XXXX'")

    def get_battery_level(self) -> int:
        """Retorna el nivel de batería actual. Retorna 0 si hay error de lectura."""
        try:
            return self.drone.get_battery()
        except Exception:
            # Si falla la lectura (dron desconectado), devolvemos 0 para no romper el programa
            return 0

    def get_frame(self):
        """
        Si hay vídeo, devuelve el frame real.
        Si NO hay vídeo, devuelve una pantalla negra (dummy) para que la UI funcione.
        """
        if config.ENABLE_VIDEO:
            return self.drone.get_frame_read().frame
        else:
            # Crea una imagen negra de 720x960 (Alto, Ancho, Canales de color)
            # Esto engaña a la interfaz para que siga funcionando sin cámara
            return np.zeros((720, 960, 3), dtype=np.uint8)

    def takeoff(self) -> None:
        self.drone.takeoff()

    def land(self) -> None:
        self.drone.land()

    def flip(self, direction: str) -> None:
        """Realiza una acrobacia controlando errores para no cerrar la app."""
        try:
            # Verificación de seguridad de batería antes de intentar
            bat = self.get_battery_level()
            if bat < 50:
                print(f"⚠️ Batería baja ({bat}%). Flips deshabilitados por seguridad.")
                return

            print(f"🤸 Intentando acrobacia: {direction}...")
            self.drone.flip(direction)

        except Exception as e:
            # Capturamos el error pero NO cerramos el programa
            print(f"❌ El dron rechazó la acrobacia: {e}")

    def toggle_mode(self) -> None:
        self.is_vertical_mode = not self.is_vertical_mode
        mode_name = "VERTICAL/ROTACIÓN" if self.is_vertical_mode else "HORIZONTAL"
        print(f"🔄 Modo cambiado a: {mode_name}")

    def update_velocities(self, lr: int, fb: int, ud: int, yv: int) -> None:
        self.rc_velocities = {'lr': lr, 'fb': fb, 'ud': ud, 'yv': yv}

    def send_rc_command(self) -> None:
        self.drone.send_rc_control(
            self.rc_velocities['lr'],
            self.rc_velocities['fb'],
            self.rc_velocities['ud'],
            self.rc_velocities['yv']
        )

    def disconnect(self) -> None:
        if config.ENABLE_VIDEO:
            self.drone.streamoff()
        self.drone.end()
