@patch('drone_manager.Tello')
def test_audit_sequence_logic(MockTello):
    """
    Simula la coreografía exacta solicitada:
    Takeoff -> Rotate 90 -> Flip L -> Flip R -> Land
    """
    # Setup
    manager = TelloDrone()
    mock_drone_instance = manager.drone # Accedemos al objeto mockeado interno
    
    # Simulación de ejecución (lo que haríamos en el script real)
    manager.takeoff()
    mock_drone_instance.rotate_clockwise(90)
    manager.flip("l")
    manager.flip("r")
    manager.land()
    
    # VERIFICACIONES (Auditoría)
    # 1. ¿Se llamó a despegar?
    manager.drone.takeoff.assert_called()
    
    # 2. ¿Se rotó 90 grados?
    manager.drone.rotate_clockwise.assert_called_with(90)
    
    # 3. ¿Se hicieron los flips correctos?
    # flip("l") llama internamente a la API con dirección "l"
    # Nota: Como llamamos a flip dos veces, usamos 'any_call' para verificar que ambas ocurrieron
    manager.drone.flip.assert_any_call("l")
    manager.drone.flip.assert_any_call("r")
    
    # 4. ¿Se aterrizó?
    manager.drone.land.assert_called()