# main.py
import cv2
from drone_manager import TelloDrone
from input_handler import InputHandler
from ui_manager import UserInterface

def main():
    # 1. Inicialización de clases
    my_drone = TelloDrone()
    input_mgr = InputHandler(my_drone)
    ui_mgr = UserInterface()

    print("Iniciando sistema DronTello...")
    my_drone.connect_and_setup()

    running = True
    while running:
        # A. Obtener imagen
        frame = my_drone.get_frame()
        # Redimensionamos aquí o en UI para rendimiento
        frame = cv2.resize(frame, (960, 720))

        # B. Actualizar Interfaz
        ui_mgr.draw_hud(frame, my_drone.get_battery_level(), my_drone.is_vertical_mode)
        
        # C. Mostrar y leer teclado
        key = ui_mgr.show(frame)

        # D. Procesar lógica (si key es ESC, running será False)
        running = input_mgr.process_key(key)

        # E. Enviar comandos físicos al dron (CRÍTICO: debe ser continuo)
        my_drone.send_rc_command()

    # Finalización limpia
    my_drone.land()
    my_drone.disconnect()
    ui_mgr.close()

if __name__ == "__main__":
    main()