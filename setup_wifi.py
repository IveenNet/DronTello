import time

from djitellopy import Tello


def configurar_seguridad():
    # --- 1. CONFIGURACIÓN ---
    # Escribe aquí el nombre y la contraseña que quieras ponerle
    # IMPORTANTE: La contraseña no puede estar vacía.
    NUEVO_SSID = "DronTello_Iveen"
    NUEVA_PASS = "12345678"

    print(f"🔒 INICIANDO PROTOCOLO DE SEGURIDAD...")
    print(f"   Red destino: {NUEVO_SSID}")
    print(f"   Contraseña:  {NUEVA_PASS}")

    drone = Tello()

    try:
        # 2. Conectamos al dron (usando la red actual que tenga)
        print("\n1. Conectando con el dron...")
        drone.connect()
        print(f"✅ Conectado. Batería actual: {drone.get_battery()}%")

        # 3. Enviamos las nuevas credenciales
        # Esta función envía internamente el comando para establecer SSID y Password.
        # El dron se reiniciará automáticamente después de esto.
        print("\n2. Enviando comando de configuración Wi-Fi...")
        drone.set_wifi_credentials(NUEVO_SSID, NUEVA_PASS)

        print("✅ ¡Credenciales actualizadas correctamente!")
        print("\n⚠️  EL DRON SE ESTÁ REINICIANDO...")
        print("👉 Tu PC perderá la conexión. Busca la nueva red wifi y conéctate con tu nueva contraseña.")

    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        print("   Asegúrate de estar conectado al Wi-Fi del Tello antes de ejecutar este script.")

if __name__ == "__main__":
    configurar_seguridad()
