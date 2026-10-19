# Big Brother CCTV — Camera Agent (Edge Ingest)

Agente de captura e ingesta universal para dispositivos físicos edge (Raspberry Pi, mini PCs o servidores Linux locales) encargado de codificar y transmitir vídeo en directo hacia **MediaMTX** vía RTSP mediante **FFmpeg**.

---

## 💡 ¿Cuándo se utiliza este agente?

Big Brother CCTV soporta múltiples topologías de streaming:

| Tipo de Cámara | ¿Necesita este agente? | Flujo de Ingesta |
|---|---|---|
| **Cámaras IP / NVR** (RTSP, HTTP) | ❌ No | MediaMTX realiza pull autónomo configurado desde la API. |
| **Emisión Externa** (OBS, Teléfonos, RTMP push) | ❌ No | El cliente emite directamente por RTMP/RTSP al puerto `:1935` / `:8554` de MediaMTX. |
| **Webcam USB / V4L2 Local** (`/dev/video*`) | ✅ **Sí** | Este agente captura `/dev/video0` y transmite el stream a MediaMTX. |
| **Generador Sintético SMPTE** (Pruebas) | ✅ Opcional | Este agente o FFmpeg genera barras de prueba SMPTE sin hardware de vídeo. |

---

## 🌟 Características

- **Gestión de Dispositivos V4L2**: Detección y lectura de dispositivos `/dev/video*`.
- **Codificación con FFmpeg**: Pipeline optimizado para transmisión H.264 de baja latencia con presets ultrarrápidos (`ultrafast`, `zerolatency`).
- **Heartbeat & Telemetría**: Sincronización continua con la API Core (`POST /api/cameras/heartbeat`) para reflejar el estado en el panel Telescreen.
- **Auto-reconexión Inteligente**: Reintento automático con backoff exponencial en caso de pérdida de conexión con MediaMTX.
- **Soporte Docker & Edge Linux**: Listo para ejecutarse como servicio systemd o contenedor Docker mapeando `/dev/video*`.

---

## ⚙️ Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|---|---|---|
| `CAMERA_NAME` | Identificador único de la cámara en el sistema | `default-camera` |
| `API_URL` | URL base de la API Core | `http://localhost:8080/api` |
| `INTERNAL_TOKEN` | Token secreto para autenticación de agentes internos | `internal-token-pro` |
| `MEDIAMTX_URL` | URL RTSP del servidor de medios MediaMTX | `rtsp://mediamtx:8554` |
| `VIDEO_DEVICE` | Ruta del dispositivo local de vídeo | `/dev/video0` |
| `RESOLUTION` | Resolución de codificación de salida | `1280x720` |
| `FPS` | Tasa de fotogramas por segundo | `30` |
| `CONFIG_POLL_INTERVAL`| Intervalo de consulta de configuración a la API (segundos) | `10` |

---

## 🚀 Instalación y Ejecución

### En Linux / Raspberry Pi (Nativo)

1. **Requisitos previos**:
   ```bash
   sudo apt-get update && sudo apt-get install -y ffmpeg v4l-utils python3 python3-venv
   ```

2. **Instalación de dependencias**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Ejecución**:
   ```bash
   CAMERA_NAME="salon-cctv" \
   API_URL="http://192.168.1.100:8080/api" \
   MEDIAMTX_URL="rtsp://192.168.1.100:8554" \
   python src/app.py
   ```

### En Docker
```bash
docker run -d --restart=unless-stopped \
  --device=/dev/video0:/dev/video0 \
  -e CAMERA_NAME="webcam-local" \
  -e API_URL="http://192.168.1.100:8080/api" \
  -e INTERNAL_TOKEN="internal-token-pro" \
  -e MEDIAMTX_URL="rtsp://192.168.1.100:8554" \
  --name bigbrother-camera \
  ghcr.io/big-brother-cctv/camera:latest
```

---

## 📁 Estructura del Proyecto

```
camera/
├── src/
│   ├── app.py              # Bucle principal de control y heartbeat
│   └── modules/
│       ├── config.py       # Lectura de variables de entorno y API
│       ├── device.py       # Detección y validación de dispositivos V4L2
│       └── ffmpeg.py       # Orquestador del proceso hijo FFmpeg
├── requirements.txt        # Dependencias de Python
└── Dockerfile              # Contenedor optimizado con FFmpeg
```