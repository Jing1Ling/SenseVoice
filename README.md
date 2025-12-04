<h4 align="center">
    <p>
        <b>English</b> |
        <a href="./README_zh.md">简体中文</a> |
    </p>
</h4>

# SenseVoice (SenseVoiceSmall) Docker Deployment

This directory provides a Docker and docker compose setup for SenseVoice focused on the `SenseVoiceSmall` model from FunAudioLLM. The setup targets Intel Gaudi hardware.

## What is SenseVoice?

SenseVoice is an automatic speech recognition (ASR) model series by FunAudioLLM. Here we use the compact `SenseVoiceSmall` model. See the official repo and model card:
- Repo: https://github.com/FunAudioLLM/SenseVoice
- Model: https://huggingface.co/FunAudioLLM/SenseVoiceSmall




## Getting Started

### 1. Clone the Repository

```bash
git clone https://gitee.com/intel-china/aisolution-sensevoicesmall.git
cd aisolution-sensevoicesmall
```

### 2. (Optional) Configure Proxy
If you are behind a proxy, set these environment variables before building:

```bash
export http_proxy=<your-http-proxy>
export https_proxy=<your-https-proxy>
export no_proxy=localhost,127.0.0.1
```

### 3. Build the Docker Image

```bash
docker compose build
```
Or, to pass proxy args manually:
```bash
docker build $(env | grep -E '(_proxy=|_PROXY)' | sed 's/^/--build-arg /') \
    -f Dockerfile \
    -t aisolution-sensevoice:latest .
```

### 4. Run the Container


#### Start Service (detached)
```bash
docker compose up -d
```
Runs in detached mode.

#### View Logs
```bash
docker compose logs -f
```
Or, to view logs for the specific container:
```bash
docker logs aisolution-sensevoice
```

#### Service Ready
When the WebUI is ready, you will see:
```
Running on local URL:  http://0.0.0.0:7860
```
Then open your browser and visit:
```
http://<host-ip>:7860
```

#### Stop the Service
```bash
docker compose down
```
Or, to stop only the running container:
```bash
docker stop aisolution-sensevoice
```

#### Notes
- Default command: `python webui.py` in `/workspace/SenseVoice`.
- Gaudi/Habana enabled via `runtime: habana`.
- Host networking (`network_mode: host`).
- Proxy environment variables supported.

## References
- SenseVoice: https://github.com/FunAudioLLM/SenseVoice
- SenseVoiceSmall: https://huggingface.co/FunAudioLLM/SenseVoiceSmall

