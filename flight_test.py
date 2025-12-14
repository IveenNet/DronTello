import time
from drone_manager import TelloDrone

def run_audit_test():
    """
    Ejecuta la secuencia de prueba requerida:
    Despegar -> Rotar 90 -> Flip Izq -> Flip Der -> Aterrizar
    """
    print("📋 Iniciando Auditoría de Vuelo Automático...")
    
    # 1. Inicializar
    drone = TelloDrone()
    drone.connect_and_setup()

    # Pequeña pausa de seguridad antes de empezar
    time.sleep(2)

    try:
        # 2. Despegar
        print("🚀 1. Despegando...")
        drone.takeoff()
        time.sleep(5) # Esperar a que se estabilice

        # 3. Rotar 90 grados (Sentido horario)
        # Usamos la función nativa del SDK para rotación precisa
        print("🔄 2. Rotando 90 grados...")
        drone.drone.rotate_clockwise(90) 
        time.sleep(4)

        # 4. Flip Left (Izquierda)
        print("⬅️ 3. Flip Izquierda...")
        drone.flip("l")
        time.sleep(4) # Los flips consumen mucha energía, dar tiempo

        # 5. Flip Right (Derecha)
        print("➡️ 4. Flip Derecha...")
        drone.flip("r")
        time.sleep(4)

        # 6. Aterrizar
        print("🛬 5. Aterrizando...")
        drone.land()
        
    except Exception as e:
        print(f"⚠️ Error durante la prueba: {e}")
        drone.land() # Aterrizaje de emergencia si algo falla
    finally:
        drone.disconnect()
        print("✅ Prueba finalizada.")

if __name__ == "__main__":
    run_audit_test()