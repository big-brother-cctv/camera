# Camera

This is the camera service for the Big Brother project. It handles camera device management, configuration, and streaming using Python.

## Features

- Camera device management and configuration
- Integration with the main API for registration and updates
- FFmpeg-based video streaming
- Environment-based configuration
- Docker support

## Requirements

- Python 3.11+
- FFmpeg installed on the system
- (Optional) Docker

## Installation

Clone the repository and navigate to the `camera` directory:

```sh
git clone https://github.com/big-brother-cctv/camera.git
cd camera
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Running

Start the camera service:

```sh
python src/app.py
```

## Configuration

Configuration is managed via environment variables:

- `CAMERA_NAME`: Name of the camera (default: `default-camera`)
- `API_URL`: Main API URL (default: `http://localhost:8080/api`)
- `INTERNAL_TOKEN`: Internal authentication token (default: `internal-token-dev`)
- `MEDIAMTX_URL`: RTSP URL for streaming (default: `rtsp://mediamtx.local`)
- `CONFIG_POLL_INTERVAL`: Poll interval for config updates (default: `10` seconds)

## Docker

To build and run with Docker:

```sh
docker build -t bigbrother-camera .
docker run --env-file .env bigbrother-camera
```

## Project Structure

- `src/app.py`: Main application entry point
- `src/modules/`: Core modules (`config.py`, `device.py`, `ffmpeg.py`)

## License

This project is licensed under the [GNU GPL v3](https://github.com/big-brother-cctv/camera/blob/main/LICENSE).