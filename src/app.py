import os
import time
import copy
import subprocess

from modules.config import (
    fetch_config, register_camera, configs_equal, send_heartbeat,
    CAMERA_NAME, API_URL, INTERNAL_TOKEN,
    MEDIAMTX_URL, POLL_INTERVAL
)
from modules.ffmpeg import build_cmd, run_ffmpeg
from modules.device import wait_for_device

DEFAULT_SOURCE_TYPE = os.getenv("SOURCE_TYPE", "v4l2")
DEFAULT_SOURCE_URL = os.getenv("SOURCE_URL", "")
DEFAULT_DEVICE = os.getenv("DEVICE", "/dev/video0")
CONNECTION_MODE = os.getenv("CONNECTION_MODE", "push")

def main():
    last_config = None
    ffmpeg_proc = None

    default_config = {
        "name": CAMERA_NAME,
        "sourceType": DEFAULT_SOURCE_TYPE,
        "sourceUrl": DEFAULT_SOURCE_URL,
        "connectionMode": CONNECTION_MODE,
        "device": DEFAULT_DEVICE,
        "resolution": os.getenv("RESOLUTION", "640x480"),
        "fps": int(os.getenv("FPS", 30)),
        "codec": "libx264",
        "preset": "ultrafast",
        "tune": "zerolatency",
        "buffer": "1000000",
        "rotation": 0
    }

    print(f"[INGSOC CAMERA AGENT] Iniciando nodo '{CAMERA_NAME}' en modo {CONNECTION_MODE.upper()}...")

    while True:
        is_running = ffmpeg_proc is not None and ffmpeg_proc.poll() is None
        hb_data = {
            "name": CAMERA_NAME,
            "sourceType": DEFAULT_SOURCE_TYPE,
            "connectionMode": CONNECTION_MODE,
            "resolution": str(default_config["resolution"]),
            "fps": str(default_config["fps"]),
            "device": DEFAULT_DEVICE,
            "status": "online" if is_running else "standby"
        }

        # Enviar heartbeat a la API central para auto-anuncio y telemetría
        server_config = send_heartbeat(hb_data)

        # Si el servidor no devolvió config mediante heartbeat, intentamos fetch_config
        config = server_config or fetch_config(CAMERA_NAME)
        if not config:
            print("[INGSOC] No se encontró directiva en API central. Auto-registrando nodo...")
            register_camera(default_config)
            time.sleep(5)
            continue

        if last_config is None or not configs_equal(config, last_config):
            if ffmpeg_proc:
                print("[INGSOC] Directiva de transmisión actualizada desde la central. Reiniciando pipeline...")
                ffmpeg_proc.terminate()
                try:
                    ffmpeg_proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    ffmpeg_proc.kill()
            cmd, target_source, postUrl, source_type = build_cmd(config)
            wait_for_device(target_source, source_type)
            ffmpeg_proc = run_ffmpeg(cmd)
            last_config = copy.deepcopy(config)
        else:
            if ffmpeg_proc and ffmpeg_proc.poll() is not None:
                print("[INGSOC] Pipeline FFmpeg interrumpido. Restableciendo enlace...")
                cmd, target_source, postUrl, source_type = build_cmd(config)
                wait_for_device(target_source, source_type)
                ffmpeg_proc = run_ffmpeg(cmd)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
