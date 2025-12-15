# 🚁 DronTello

**Sistema de control de vuelo modular para DJI Tello basado en Python y OpenCV.**

Este proyecto implementa un controlador de vuelo completo para el dron **Ryze/DJI Tello**. A diferencia de scripts básicos, `DronTello` utiliza una arquitectura orientada a objetos (OOP) y principios SOLID para desacoplar la lógica de vuelo, la gestión de entrada (teclado) y la interfaz de usuario (HUD de vídeo).

Puedes descargar la última versión compilada en la sección "Actions" o "Releases".

![Build Status](https://github.com/IveenNet/DronTello/actions/workflows/build_windows.yml/badge.svg)

---

## 🚀 Características Principales

* **Transmisión de Vídeo Configurable:** Soporte para feed de cámara en tiempo real (desactivado por defecto para máxima compatibilidad).
* **Telemetría en Pantalla (HUD):** Monitorización en tiempo real del nivel de batería y modo de vuelo.
* **Control de Vuelo Dual:**
  * *Modo Estándar:* Movimiento horizontal (adelante, atrás, izquierda, derecha).
  * *Modo Altitud/Rotación:* Control de altura y guiñada (yaw) para ajustes precisos.
* **Acrobacias:** Ejecución de flips (volteretas) preprogramadas.
* **Seguridad Wi-Fi:** Herramientas incluidas para proteger la red del dron con contraseña WPA2.
* **Arquitectura Modular:** Código organizado en clases independientes.

## 🛠️ Arquitectura del Proyecto

El código está estructurado siguiendo el principio de responsabilidad única (SRP):

| Archivo | Responsabilidad |
| :--- | :--- |
| `main.py` | Punto de entrada. Orquesta el bucle principal. |
| `drone_manager.py` | Wrapper de la API `djitellopy`. Maneja la conexión y comandos de hardware. |
| `input_handler.py` | Procesa eventos de teclado y define la lógica de control. |
| `ui_manager.py` | Gestiona la ventana de OpenCV y dibuja la interfaz (HUD). |
| `config.py` | **Configuración central.** Controla la activación de cámara, velocidades y constantes. |
| `setup_wifi.py` | Script de utilidad para establecer/cambiar la contraseña del Wi-Fi. |

## ⚙️ Configuración y Seguridad

### 1. Activar la Cámara

Por defecto, el vídeo está **desactivado** (`False`) para asegurar la compatibilidad con firewalls de Windows y redes corporativas.

Para activar la cámara:

1. Abre el archivo `config.py`.
2. Cambia la variable `ENABLE_VIDEO` a `True`:

    ```python
    ENABLE_VIDEO: bool = True
    ```

3. Guarda y ejecuta `main.py`.

### 2. Proteger el Wi-Fi del Dron (Contraseña)

El Tello viene con una red abierta de fábrica. Para ponerle contraseña:

1. Abre el archivo `setup_wifi.py`.
2. Edita las variables con tu configuración deseada:

    ```python
    NUEVO_SSID = "MiDronPrivado"
    NUEVA_PASS = "MiContraseñaSegura"
    ```

3. Conéctate al dron y ejecuta el script una sola vez:

    ```bash
    python setup_wifi.py
    ```

4. El dron se reiniciará. Deberás volver a conectar tu PC usando la nueva contraseña.

> **Resetear Wi-Fi:** Si olvidas la contraseña, enciende el dron y mantén pulsado el botón de encendido durante 5 segundos para volver a la configuración abierta de fábrica.

## 📋 Requisitos e Instalación

1. **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/IveenNet/DronTello.git](https://github.com/IveenNet/DronTello.git)
    cd DronTello
    ```

2. **Instalar dependencias:**
    Asegúrate de tener Python 3.x instalado. Luego, ejecuta:

    ```bash
    pip install -r requirements.txt
    ```

3. **Conexión:**
    * Enciende tu DJI Tello.
    * Conéctate a la red Wi-Fi del dron (ej. `TELLO-XXXXX` o tu red personalizada).

## 🎮 Controles de Vuelo

El sistema utiliza la ventana de la aplicación para capturar el teclado. **Debes tener la ventana (negra o vídeo) seleccionada**.

### Teclas Globales

| Tecla | Acción | Descripción |
| :---: | :--- | :--- |
| **T** | Takeoff | Despegar el dron. |
| **L** | Land | Aterrizar suavemente. |
| **ESC** | Salir | Aterriza y cierra el programa. |
| **Q** | **Cambiar Modo** | Alterna entre movimiento horizontal y vertical/rotación. |

### Modos de Vuelo (Alternar con 'Q')

| Tecla | Modo 1: Horizontal (LED Verde en HUD) | Modo 2: Vertical/Giro (LED Rojo en HUD) |
| :---: | :--- | :--- |
| **W** | Avanzar | Subir Altura (Ascender) |
| **S** | Retroceder | Bajar Altura (Descender) |
| **A** | Desplazar Izquierda (Roll) | Girar Izquierda (Yaw) |
| **D** | Desplazar Derecha (Roll) | Girar Derecha (Yaw) |

### Acrobacias

* **F**: Flip hacia adelante (Forward).
* **B**: Flip hacia atrás (Back).
* **Z**: Flip hacia la izquierda (Left).
* **X**: Flip hacia la derecha (Right).

## 🧪 Auditoría y Pruebas (QA)

### 1. Pruebas Unitarias (Simulación)

Tests automatizados que verifican la lógica sin conectar el dron.

```bash
pytest
```

## Script de Auditoría de Vuelo (Prueba Física)

Script autónomo que realiza la secuencia: Despegue -> Rotación 90° -> Flips -> Aterrizaje. ⚠️ Precaución: Requiere espacio de 3x3 metros.

```bash
python flight_test.py
```

## ⚠️ Advertencia de Seguridad

* Este software se proporciona "tal cual". El desarrollador no se hace responsable de daños al dron o al entorno.
* Asegúrate de volar en un área despejada e interior (el Tello es sensible al viento).
* Utiliza protectores de hélices siempre que sea posible.

---
*Desarrollado con ❤️ usando la API oficial de Tello.*
