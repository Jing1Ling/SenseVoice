<h4 align="center">
    <p>
        <a href="./README.md">English</a> |
        <b>简体中文</b> |
    </p>
</h4>

# SenseVoice（SenseVoiceSmall）Docker 部署
本目录提供适用于 Intel Gaudi（Habana）硬件的 SenseVoice Docker 与 docker compose 部署方式，聚焦 `SenseVoiceSmall` 模型，开箱即用、便于快速上手。

## SenseVoice 简介
SenseVoice 是 FunAudioLLM 推出的自动语音识别（ASR）模型系列。本文档聚焦体量较小的 `SenseVoiceSmall` 模型。
- 官方仓库：https://github.com/FunAudioLLM/SenseVoice
- 模型卡：https://huggingface.co/FunAudioLLM/SenseVoiceSmall

## 开始使用

### 1. 克隆仓库
```bash
git clone https://gitee.com/intel-china/aisolution-sensevoicesmall.git
cd aisolution-sensevoicesmall
```

### 2. （可选）配置代理
若处于代理环境，构建镜像前请设置以下环境变量：
```bash
export http_proxy=<your-http-proxy>
export https_proxy=<your-https-proxy>
export no_proxy=localhost,127.0.0.1
```

### 3. 构建 Docker 镜像
```bash
docker compose build
```
或使用手动传递代理参数的方式：
```bash
docker build $(env | grep -E '(_proxy=|_PROXY)' | sed 's/^/--build-arg /') \
    -f Dockerfile \
    -t aisolution-sensevoice:latest .
```

### 4. 运行容器
#### 启动服务（后台）
```bash
docker compose up -d
```
以 detached 模式运行。

#### 查看日志
```bash
docker compose logs -f
```
或查看指定容器日志：
```bash
docker logs aisolution-sensevoice
```

#### 服务就绪
当 WebUI 就绪时，你会看到：
```
Running on local URL:  http://0.0.0.0:7860
```
随后可通过浏览器访问：
```
http://<host-ip>:7860
```

#### 停止服务
```bash
docker compose down
```
或仅停止容器：
```bash
docker stop aisolution-sensevoice
```

#### 说明
- 默认命令：在 `/workspace/SenseVoice` 目录下运行 `python webui.py`。
- 通过 `runtime: habana` 启用 Gaudi/Habana。
- 主机网络（`network_mode: host`）。
- 支持代理环境变量。

## 参考
- 官方仓库：https://github.com/FunAudioLLM/SenseVoice
- 模型卡：https://huggingface.co/FunAudioLLM/SenseVoiceSmall
