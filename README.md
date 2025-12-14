# 🚁 DronTello

**Sistema de control de vuelo modular para DJI Tello basado en Python y OpenCV.**

Este proyecto implementa un controlador de vuelo completo para el dron **Ryze/DJI Tello**. A diferencia de scripts básicos, `DronTello` utiliza una arquitectura orientada a objetos (OOP) y principios SOLID para desacoplar la lógica de vuelo, la gestión de entrada (teclado) y la interfaz de usuario (HUD de vídeo).

Puedes descargar la última versión compilada en la sección "Actions" o "Releases"

![Build Status](https://github.com/IveenNet/DronTello/actions/workflows/build_windows.yml/badge.svg)

---

## 🚀 Características Principales

* **Transmisión de Vídeo en Tiempo Real:** Visualización del feed de la cámara del Tello con baja latencia.
* **Telemetría en Pantalla (HUD):** Monitorización en tiempo real del nivel de batería y modo de vuelo.
* **Control de Vuelo Dual:**
    * *Modo Estándar:* Movimiento horizontal (adelante, atrás, izquierda, derecha).
    * *Modo Altitud/Rotación:* Control de altura y guiñada (yaw) para ajustes precisos.
* **Acrobacias:** Ejecución de flips (volteretas) preprogramadas.
* **Arquitectura Modular:** Código organizado en clases independientes para facilitar la escalabilidad y el mantenimiento.

## 🛠️ Arquitectura del Proyecto

El código está estructurado siguiendo el principio de responsabilidad única (SRP):

| Archivo | Responsabilidad |
| :--- | :--- |
| `main.py` | Punto de entrada. Orquesta el bucle principal. |
| `drone_manager.py` | Wrapper de la API `djitellopy`. Maneja la conexión y comandos de hardware. |
| `input_handler.py` | Procesa eventos de teclado y define la lógica de control. |
| `ui_manager.py` | Gestiona la ventana de OpenCV y dibuja la interfaz (HUD). |
| `config.py` | Almacena constantes de configuración (velocidades, colores, etc.). |

## 📋 Requisitos e Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/IveenNet/DronTello.git](https://github.com/IveenNet/DronTello.git)
    cd DronTello
    ```

2.  **Instalar dependencias:**
    Asegúrate de tener Python 3.x instalado. Luego, ejecuta el siguiente comando para instalar automáticamente todas las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Conexión:**
    * Enciende tu DJI Tello.
    * Conéctate a la red Wi-Fi del dron (ej. `TELLO-XXXXX`).

## 🎮 Controles de Vuelo

El sistema utiliza la librería OpenCV para capturar el teclado, por lo que **la ventana de vídeo debe estar activa** (seleccionada) para que funcionen los controles.

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

Este proyecto incluye un sistema de aseguramiento de calidad para garantizar la estabilidad del vuelo sin poner en riesgo el hardware.

### 1. Pruebas Unitarias (Simulación)
El proyecto cuenta con tests automatizados utilizando `pytest` y `unittest.mock`. Estas pruebas verifican la lógica interna del código sin necesidad de conectar el dron.

Para ejecutar la suite de pruebas:
```bash
pytest
```

## ⚠️ Advertencia de Seguridad

* Este software se proporciona "tal cual". El desarrollador no se hace responsable de daños al dron o al entorno.
* Asegúrate de volar en un área despejada e interior (el Tello es sensible al viento).
* Utiliza protectores de hélices siempre que sea posible.

---
*Desarrollado con ❤️ usando la API oficial de Tello.*