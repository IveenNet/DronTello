# ui_manager.py
import cv2

import config


class UserInterface:
    """
    Maneja la ventana y el HUD (Heads-Up Display).
    """
    def __init__(self):
        self.window_name = config.WINDOW_NAME

    def draw_hud(self, frame, battery: int, mode_vertical: bool):
        # Texto del Modo
        mode_text = "MODO: ALTURA/GIRO" if mode_vertical else "MODO: HORIZONTAL"
        color_mode = (0, 0, 255) if mode_vertical else (0, 255, 0)

        cv2.putText(frame, mode_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, color_mode, 2)

        # Texto de Batería
        cv2.putText(frame, f"BAT: {battery}%", (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, config.FONT_COLOR, 2)

        # Instrucciones pie de página
        cv2.putText(frame, "'Q': Cambiar Modo | 'T': Despegar | 'L': Aterrizar",
                    (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_PLAIN, 1, config.FONT_COLOR, 1)

    def show(self, frame) -> int:
        """Muestra el frame y devuelve la tecla pulsada."""
        cv2.imshow(self.window_name, frame)
        return cv2.waitKey(1) & 0xff

    def close(self):
        cv2.destroyAllWindows()
