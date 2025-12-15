import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Añadimos la carpeta raíz al path para poder importar tus módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from drone_manager import TelloDrone
from input_handler import InputHandler

# --- PRUEBAS PARA DRONE_MANAGER ---

@patch('drone_manager.Tello')  # 1. Simulamos la clase Tello original
def test_drone_initialization(MockTello):
    """Prueba que el dron se inicializa correctamente."""
    manager = TelloDrone()

    # Verificamos que se creó una instancia del Tello falso
    assert manager.drone is not None
    # Verificamos que el modo empieza en Horizontal (False)
    assert manager.is_vertical_mode is False

@patch('drone_manager.Tello')
def test_toggle_mode(MockTello):
    """Prueba que el cambio de modo (Q) funciona."""
    manager = TelloDrone()

    # Estado inicial: False
    manager.toggle_mode()
    assert manager.is_vertical_mode is True  # Debe cambiar a True

    manager.toggle_mode()
    assert manager.is_vertical_mode is False # Debe volver a False

@patch('drone_manager.Tello')
def test_send_rc_command(MockTello):
    """Prueba que se envían los comandos correctos al SDK."""
    manager = TelloDrone()
    # Mockeamos el método send_rc_control del objeto interno
    manager.drone.send_rc_control = MagicMock()

    # Simulamos unas velocidades
    manager.update_velocities(10, 20, 30, 40)
    manager.send_rc_command()

    # VERIFICACIÓN CLAVE: ¿Se llamó a la función con estos números?
    manager.drone.send_rc_control.assert_called_with(10, 20, 30, 40)


# --- PRUEBAS PARA INPUT_HANDLER ---
@patch('drone_manager.Tello')
def test_input_takeoff(MockTello):
    """Prueba que la tecla T llama a takeoff."""
    # Setup
    drone_mgr = TelloDrone()
    drone_mgr.takeoff = MagicMock() # Espiamos esta función
    handler = InputHandler(drone_mgr)

    # Acción: Simular pulsar 't'
    handler.process_key(ord('t'))

    # Assert: Verificar que se llamó al despegue
    drone_mgr.takeoff.assert_called_once()

@patch('drone_manager.Tello')
def test_input_movement_horizontal(MockTello):
    """Prueba que W mueve hacia ADELANTE en modo horizontal."""
    drone_mgr = TelloDrone()
    drone_mgr.is_vertical_mode = False # Aseguramos modo horizontal
    handler = InputHandler(drone_mgr)

    # Acción: Simular pulsar 'w'
    handler.process_key(ord('w'))

    # Assert: Debe haber velocidad en 'fb' (forward/back) pero 0 en 'ud' (up/down)
    assert drone_mgr.rc_velocities['fb'] == config.SPEED
    assert drone_mgr.rc_velocities['ud'] == 0

@patch('drone_manager.Tello')
def test_input_movement_vertical(MockTello):
    """Prueba que W mueve hacia ARRIBA en modo vertical."""
    drone_mgr = TelloDrone()
    drone_mgr.toggle_mode() # Cambiamos a modo vertical
    handler = InputHandler(drone_mgr)

    # Acción: Simular pulsar 'w'
    handler.process_key(ord('w'))

    # Assert: Ahora 'fb' debe ser 0 y 'ud' debe tener velocidad
    assert drone_mgr.rc_velocities['fb'] == 0
    assert drone_mgr.rc_velocities['ud'] == config.SPEED

@patch('drone_manager.Tello')
def test_audit_sequence_logic(MockTello):
    """
    Simula la coreografía exacta solicitada:
    Takeoff -> Rotate 90 -> Flip L -> Flip R -> Land
    """
    # 1. Setup
    manager = TelloDrone()

    # --- CORRECCIÓN IMPORTANTE ---
    # Simulamos que la batería está al 100%.
    # Sin esto, get_battery() devuelve un objeto Mock y falla la comparación (Mock < 50)
    manager.drone.get_battery.return_value = 100
    # -----------------------------

    # 2. Simulación de ejecución
    manager.takeoff()
    manager.drone.rotate_clockwise(90)
    manager.flip("l")
    manager.flip("r")
    manager.land()

    # 3. VERIFICACIONES (Auditoría)

    # ¿Se llamó a despegar?
    manager.drone.takeoff.assert_called()

    # ¿Se rotó 90 grados?
    manager.drone.rotate_clockwise.assert_called_with(90)

    # ¿Se hicieron los flips correctos?
    # Ahora sí pasará porque la batería es "100" y entra en el if
    manager.drone.flip.assert_any_call("l")
    manager.drone.flip.assert_any_call("r")

    # ¿Se aterrizó?
    manager.drone.land.assert_called()
