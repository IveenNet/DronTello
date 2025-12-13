# input_handler.py
import cv2
from drone_manager import TelloDrone
import config

class InputHandler:
    """
    Procesa el teclado y actualiza el estado del dron.
    """
    def __init__(self, drone: TelloDrone):
        self.drone = drone

    def process_key(self, key_code: int) -> bool:
        """Retorna False si se debe salir de la app (ESC)."""
        
        # Reiniciar velocidades a 0 (Dead man switch)
        lr, fb, ud, yv = 0, 0, 0, 0
        
        # --- Comandos de Sistema ---
        if key_code == 27:  # Tecla ESC
            return False
        
        # --- Comandos Directos ---
        if key_code == ord('t'): self.drone.takeoff()
        if key_code == ord('l'): self.drone.land()
        if key_code == ord('q'): self.drone.toggle_mode()
        
        # --- Acrobacias (Flips) ---
        #direction: l, r, f, b
        if key_code == ord('f'): self.drone.flip("f") 
        if key_code == ord('b'): self.drone.flip("b")

        # --- Movimiento ---
        speed = config.SPEED
        rot_speed = config.ROTATION_SPEED

        if not self.drone.is_vertical_mode:
            # MODO HORIZONTAL
            if key_code == ord('w'): fb = speed
            elif key_code == ord('s'): fb = -speed
            if key_code == ord('a'): lr = -speed
            elif key_code == ord('d'): lr = speed
        else:
            # MODO VERTICAL
            if key_code == ord('w'): ud = speed
            elif key_code == ord('s'): ud = -speed
            if key_code == ord('a'): yv = -rot_speed
            elif key_code == ord('d'): yv = rot_speed

        self.drone.update_velocities(lr, fb, ud, yv)
        return True